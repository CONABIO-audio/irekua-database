from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from hypothesis import given
from hypothesis import strategies
from hypothesis import assume
from hypothesis.extra.django import TestCase

from irekua_terms.models import TermType
from irekua_terms.models import Term
from irekua_terms.models import EntailmentType
from irekua_terms.models import Entailment


valid_string = lambda: strategies.text(
    alphabet=strategies.characters(
        blacklist_categories=("Cs", "Cc"),
    ),
    min_size=5,
)

random_entailment_metadata = lambda: strategies.fixed_dictionaries(
    {"prop3": valid_string()}
)


class EntailmentTypeTestCase(TestCase):
    fixtures = ["irekua_terms/categorical.json", "irekua_terms/boolean.json"]

    def setUp(self):
        self.cat1 = TermType.objects.get(name="categorical1")
        self.cat2 = TermType.objects.get(name="categorical2")
        self.boolean = TermType.objects.get(name="boolean")

    @given(
        source_value=valid_string(),
        target_value=valid_string(),
        metadata=random_entailment_metadata(),
    )
    def test_repr(self, source_value, target_value, metadata):
        source = Term.objects.create(term_type=self.cat1, value=source_value)
        target = Term.objects.create(term_type=self.cat2, value=target_value)
        entailment = Entailment.objects.create(
            source=source, target=target, metadata=metadata
        )

        self.assertEqual(
            str(entailment),
            f"{source} => {target}",
        )

    @given(
        source_value=valid_string(),
        target_value=valid_string(),
        metadata=random_entailment_metadata(),
    )
    def test_unique_together(self, source_value, target_value, metadata):
        source = Term.objects.create(term_type=self.cat1, value=source_value)
        target = Term.objects.create(term_type=self.cat2, value=target_value)

        Entailment.objects.create(
            source=source, target=target, metadata=metadata
        )

        with self.assertRaises(IntegrityError):
            Entailment.objects.create(
                source=source, target=target, metadata=metadata
            )

    @given(
        value1=valid_string(),
        value2=valid_string(),
        boolean_value=strategies.booleans(),
        metadata=random_entailment_metadata(),
    )
    def test_clean_exists_entailment_type(
        self, value1, value2, boolean_value, metadata
    ):
        term1, _ = Term.objects.get_or_create(
            term_type=self.cat1, value=value1
        )
        term2, _ = Term.objects.get_or_create(
            term_type=self.cat2, value=value2
        )
        boolean_term, _ = Term.objects.get_or_create(
            term_type=self.boolean, value=boolean_value
        )

        Entailment(source=term1, target=term2, metadata=metadata).clean()

        with self.assertRaises(EntailmentType.DoesNotExist):
            EntailmentType.objects.get(target_type=self.boolean)

        with self.assertRaises(ValidationError):
            Entailment(source=term1, target=boolean_term).clean()

    @given(
        value1=valid_string(),
        value2=valid_string(),
        metadata=random_entailment_metadata(),
    )
    def test_clean_valid_metadata(self, value1, value2, metadata):
        term1, _ = Term.objects.get_or_create(
            term_type=self.cat1, value=value1
        )
        term2, _ = Term.objects.get_or_create(
            term_type=self.cat2, value=value2
        )

        Entailment(source=term1, target=term2, metadata=metadata).clean()

    @given(
        value1=valid_string(),
        value2=valid_string(),
        metadata=strategies.dictionaries(
            strategies.text(),
            strategies.text(),
        ),
    )
    def test_clean_invalid_metadata(self, value1, value2, metadata):
        assume("prop3" not in metadata)

        term1, _ = Term.objects.get_or_create(
            term_type=self.cat1, value=value1
        )
        term2, _ = Term.objects.get_or_create(
            term_type=self.cat2, value=value2
        )

        with self.assertRaises(ValidationError):
            Entailment(source=term1, target=term2, metadata=metadata).clean()
