from django.core.exceptions import ValidationError
from hypothesis import given
from hypothesis import strategies
from hypothesis import assume
from hypothesis.extra.django import TestCase

from irekua_terms.models import TermType
from irekua_terms.models import TermSuggestion
from irekua_database.models import User


valid_string = lambda: strategies.text(
    alphabet=strategies.characters(
        blacklist_categories=('Cs', 'Cc'),
    ),
    min_size=5,
)


class TermSuggestionTestCase(TestCase):
    fixtures = [
        'irekua_database/users.json',
        'irekua_terms/categorical.json',
        'irekua_terms/boolean.json',
        'irekua_terms/integer.json',
        'irekua_terms/numeric.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='regular')
        self.categorical = TermType.objects.get(name='categorical1')
        self.boolean = TermType.objects.get(name='boolean')
        self.integer = TermType.objects.get(name='integer')
        self.numeric = TermType.objects.get(name='numeric')

    @given(valid_string())
    def test_repr(self, value):
        suggestion = TermSuggestion(
            term_type=self.categorical,
            value=value,
            created_by=self.user,
        )
        self.assertEqual(
            str(suggestion),
            f'categorical1: {value}'
        )

    @given(valid_string())
    def test_clean_non_categorical_types(self, value):
        with self.assertRaises(ValidationError):
            TermSuggestion(
                term_type=self.boolean,
                value=value,
                metadata=None).clean()

        with self.assertRaises(ValidationError):
            TermSuggestion(
                term_type=self.integer,
                value=value,
                metadata=None).clean()

        with self.assertRaises(ValidationError):
            TermSuggestion(
                term_type=self.numeric,
                value=value,
                metadata=None).clean()

    @given(
        value=valid_string(),
        metadata=strategies.fixed_dictionaries({
            'prop1': strategies.text(),
        })
    )
    def test_clean_valid_metadata(self, value, metadata):
        TermSuggestion(
            term_type=self.categorical,
            value=value,
            metadata=metadata).clean()

    @given(
        value=valid_string(),
        metadata=strategies.dictionaries(strategies.text(), strategies.text())
    )
    def test_clean_invalid_metadata(self, value, metadata):
        assume('prop1' not in metadata)

        with self.assertRaises(ValidationError):
            TermSuggestion(
                term_type=self.categorical,
                value=value,
                metadata=metadata).clean()
