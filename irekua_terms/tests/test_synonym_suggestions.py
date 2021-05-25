from django.core.exceptions import ValidationError

from hypothesis import given
from hypothesis import strategies
from hypothesis import assume
from hypothesis.extra.django import TestCase

from irekua_terms.models import TermType
from irekua_terms.models import Term
from irekua_terms.models import SynonymSuggestion
from irekua_database.models import User


valid_string = lambda: strategies.text(
    alphabet=strategies.characters(
        blacklist_categories=("Cs", "Cc"),
    ),
    min_size=5,
)


class SynonymSuggestionTestCase(TestCase):
    fixtures = [
        "irekua_database/users.json",
        "irekua_terms/categorical.json",
        "irekua_terms/boolean.json",
        "irekua_terms/integer.json",
        "irekua_terms/numeric.json",
    ]

    def setUp(self):
        self.user = User.objects.get(username="regular")
        self.categorical = TermType.objects.get(name="categorical1")
        self.boolean = TermType.objects.get(name="boolean")
        self.integer = TermType.objects.get(name="integer")
        self.numeric = TermType.objects.get(name="numeric")
        self.term = Term.objects.filter(term_type=self.categorical).first()

    @given(valid_string())
    def test_repr(self, value):
        suggestion = SynonymSuggestion(
            source=self.term, synonym=value, created_by=self.user
        )

        self.assertEqual(str(suggestion), f"{self.term} = {value}")

    @given(strategies.integers())
    def test_clean_integer_types(self, value):
        term, _ = Term.objects.get_or_create(
            term_type=self.integer, value=value
        )

        with self.assertRaises(ValidationError):
            SynonymSuggestion(
                source=term, synonym=value, created_by=self.user
            ).clean()

    @given(strategies.booleans())
    def test_clean_boolean_types(self, value):
        term, _ = Term.objects.get_or_create(
            term_type=self.boolean, value=value
        )

        with self.assertRaises(ValidationError):
            SynonymSuggestion(
                source=term, synonym=value, created_by=self.user
            ).clean()

    @given(strategies.floats())
    def test_clean_numeric_types(self, value):
        term, _ = Term.objects.get_or_create(
            term_type=self.numeric, value=value
        )

        with self.assertRaises(ValidationError):
            SynonymSuggestion(
                source=term, synonym=value, created_by=self.user
            ).clean()

    @given(
        value=valid_string(),
        metadata=strategies.fixed_dictionaries(
            {
                "prop2": strategies.text(),
            }
        ),
    )
    def test_clean_valid_metadata(self, value, metadata):
        SynonymSuggestion(
            source=self.term, synonym=value, metadata=metadata
        ).clean()

    @given(
        value=valid_string(),
        metadata=strategies.dictionaries(strategies.text(), strategies.text()),
    )
    def test_clean_invalid_metadata(self, value, metadata):
        assume("prop2" not in metadata)

        with self.assertRaises(ValidationError):
            SynonymSuggestion(
                source=self.term, synonym=value, metadata=metadata
            ).clean()
