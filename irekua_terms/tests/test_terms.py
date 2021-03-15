from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from hypothesis import given
from hypothesis import strategies
from hypothesis import assume
from hypothesis.extra.django import TestCase

from irekua_terms.models import TermType
from irekua_terms.models import Term
from irekua_terms.models import Entailment


valid_string = lambda: strategies.text(
    alphabet=strategies.characters(
        blacklist_categories=("Cs", "Cc"),
    ),
    min_size=5,
)


class TermTestCase(TestCase):
    fixtures = [
        "irekua_terms/categorical.json",
        "irekua_terms/numeric.json",
        "irekua_terms/integer.json",
        "irekua_terms/boolean.json",
    ]

    def setUp(self):
        self.categorical = TermType.objects.get(name="categorical1")
        self.numerical = TermType.objects.get(name="numeric")
        self.integer = TermType.objects.get(name="integer")
        self.boolean = TermType.objects.get(name="boolean")

    @given(valid_string())
    def test_repr(self, value):
        term = Term(term_type=self.categorical, value=value)
        self.assertEqual(str(term), f"categorical1: {value}")

    @given(valid_string())
    def test_unique_value(self, value):
        Term.objects.create(term_type=self.categorical, value=value)

        with self.assertRaises(IntegrityError):
            Term.objects.create(term_type=self.categorical, value=value)

    @given(value=valid_string(), scope=valid_string())
    def test_unique_value_with_scope(self, value, scope):
        Term.objects.create(
            term_type=self.categorical, value=value, scope=scope
        )

        Term.objects.create(term_type=self.categorical, value=value)

        with self.assertRaises(IntegrityError):
            Term.objects.create(
                term_type=self.categorical, value=value, scope=scope
            )

    @given(
        value=valid_string(),
        metadata=strategies.fixed_dictionaries({"prop1": strategies.text()}),
    )
    def test_categorical_clean_valid(self, value, metadata):
        term = Term(term_type=self.categorical, value=value, metadata=metadata)
        term.clean()

    @given(
        value=valid_string(),
        metadata=strategies.dictionaries(strategies.text(), strategies.text()),
    )
    def test_categorical_clean_invalid(self, value, metadata):
        assume("prop1" not in metadata)

        term = Term(term_type=self.categorical, value=value, metadata=metadata)

        with self.assertRaises(ValidationError):
            term.clean()

    @given(value=strategies.integers())
    def test_clean_integer_values(self, value):
        assume(value not in [0, 1])
        value = str(value)

        Term(term_type=self.numerical, value=value).clean()
        Term(term_type=self.integer, value=value).clean()

        with self.assertRaises(ValidationError):
            Term(term_type=self.boolean, value=value).clean()

    @given(value=strategies.floats())
    def test_clean_numeric_values(self, value):
        assume(value % 1 != 0)
        value = str(value)

        Term(term_type=self.numerical, value=value).clean()

        with self.assertRaises(ValidationError):
            Term(term_type=self.integer, value=value).clean()

        with self.assertRaises(ValidationError):
            Term(term_type=self.boolean, value=value).clean()

    @given(value=strategies.booleans())
    def test_clean_boolean_values(self, value):
        value = str(value)

        with self.assertRaises(ValidationError):
            Term(term_type=self.numerical, value=value).clean()

        with self.assertRaises(ValidationError):
            Term(term_type=self.integer, value=value).clean()

        Term(term_type=self.boolean, value=value).clean()

    @given(
        value1=valid_string(),
        value2=valid_string(),
    )
    def test_entails(self, value1, value2):
        term1, _ = Term.objects.get_or_create(
            term_type=self.categorical, value=value1
        )
        term2, _ = Term.objects.get_or_create(
            term_type=self.categorical, value=value2
        )

        self.assertFalse(term1.entails(term2))

        Entailment.objects.create(
            source=term1,
            target=term2,
        )

        self.assertTrue(term1.entails(term2))
