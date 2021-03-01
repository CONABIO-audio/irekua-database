from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from hypothesis import given
from hypothesis import strategies
from hypothesis import assume
from hypothesis.extra.django import from_model
from hypothesis.extra.django import TestCase

from irekua_terms.models import TermType
from irekua_terms.models import EntailmentType


random_term_type = lambda: from_model(
    TermType,
    metadata_schema=strategies.none(),
    synonym_metadata_schema=strategies.none(),
)


class EntailmentTypeTestCase(TestCase):
    fixtures = [
        "irekua_terms/categorical.json",
    ]

    def setUp(self):
        self.entailment_type = EntailmentType.objects.get(pk=1)

    @given(
        source=random_term_type(),
        target=random_term_type(),
    )
    def test_repr(self, source, target):
        entailment_type = EntailmentType(source_type=source, target_type=target)
        self.assertEqual(str(entailment_type), f"{source} => {target}")

    @given(
        source=random_term_type(),
        target=random_term_type(),
    )
    def test_unique_together(self, source, target):
        assume(source != target)

        EntailmentType.objects.create(source_type=source, target_type=target)

        with self.assertRaises(IntegrityError):
            EntailmentType.objects.create(source_type=source, target_type=target)

    @given(
        source=random_term_type(),
        target=random_term_type(),
    )
    def test_clean(self, source, target):
        assume(source != target)

        EntailmentType(source_type=source, target_type=target).clean()

        with self.assertRaises(ValidationError):
            EntailmentType(source_type=source, target_type=source).clean()

    @given(
        strategies.fixed_dictionaries(
            {
                "prop3": strategies.text(),
            }
        )
    )
    def test_validate_valid_metadata(self, metadata):
        self.entailment_type.validate_metadata(metadata)

    @given(strategies.dictionaries(strategies.text(), strategies.text()))
    def test_validate_invalid_metadata(self, metadata):
        assume("prop3" not in metadata)

        with self.assertRaises(ValidationError):
            self.entailment_type.validate_metadata(metadata)
