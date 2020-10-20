from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from hypothesis import given
from hypothesis import strategies
from hypothesis import assume
from hypothesis.extra.django import TestCase

from irekua_terms.models import TermType
from irekua_terms.models import Term
from irekua_terms.models import Synonym


valid_string = lambda: strategies.text(
    alphabet=strategies.characters(
        blacklist_categories=('Cs', 'Cc'),
    ),
    min_size=5,
)


class SynonymsTestCase(TestCase):
    fixtures = [
        'irekua_terms/categorical.json',
        'irekua_terms/numeric.json',
        'irekua_terms/integer.json',
        'irekua_terms/boolean.json',
    ]

    def setUp(self):
        self.categorical = TermType.objects.get(name='categorical1')
        self.categorical2 = TermType.objects.get(name='categorical2')
        self.integer = TermType.objects.get(name='integer')
        self.boolean = TermType.objects.get(name='boolean')
        self.numeric = TermType.objects.get(name='numeric')

    @given(
        value1=valid_string(),
        value2=valid_string(),
    )
    def test_repr(self, value1, value2):
        term1, _ = Term.objects.get_or_create(
            term_type=self.categorical,
            value=value1)
        term2, _ = Term.objects.get_or_create(
            term_type=self.categorical,
            value=value2)
        synonym = Synonym(source=term1, target=term2)

        self.assertEqual(
            str(synonym),
            f'{term1} = {term2}'
        )

    @given(
        value1=valid_string(),
        value2=valid_string(),
    )
    def test_unique_together(self, value1, value2):
        term1, _ = Term.objects.get_or_create(
            term_type=self.categorical,
            value=value1)
        term2, _ = Term.objects.get_or_create(
            term_type=self.categorical,
            value=value2)

        Synonym.objects.create(source=term1, target=term2)

        with self.assertRaises(IntegrityError):
            Synonym.objects.create(source=term1, target=term2)

    @given(
        value1=valid_string(),
        value2=valid_string(),
        value3=valid_string(),
    )
    def test_clean_same_type(self, value1, value2, value3):
        term1, _ = Term.objects.get_or_create(
            term_type=self.categorical,
            value=value1)
        term2, _ = Term.objects.get_or_create(
            term_type=self.categorical,
            value=value2)
        term3, _ = Term.objects.get_or_create(
            term_type=self.categorical2,
            value=value3)

        self.assertTrue(self.categorical != self.categorical2)

        Synonym(source=term1, target=term2).save()

        with self.assertRaises(ValidationError):
            Synonym(source=term1, target=term3).clean()

    @given(
        value1=strategies.integers(),
        value2=strategies.integers(),
    )
    def test_clean_integer_type(self, value1, value2):
        term1, _ = Term.objects.get_or_create(
            term_type=self.integer,
            value=value1)
        term2, _ = Term.objects.get_or_create(
            term_type=self.integer,
            value=value2)

        with self.assertRaises(ValidationError):
            Synonym(source=term1, target=term2).clean()

    @given(
        value1=strategies.floats(),
        value2=strategies.floats(),
    )
    def test_clean_numeric_type(self, value1, value2):
        term1, _ = Term.objects.get_or_create(
            term_type=self.numeric,
            value=value1)
        term2, _ = Term.objects.get_or_create(
            term_type=self.numeric,
            value=value2)

        with self.assertRaises(ValidationError):
            Synonym(source=term1, target=term2).clean()

    @given(
        value1=strategies.booleans(),
        value2=strategies.booleans(),
    )
    def test_clean_boolean_type(self, value1, value2):
        term1, _ = Term.objects.get_or_create(
            term_type=self.boolean,
            value=value1)
        term2, _ = Term.objects.get_or_create(
            term_type=self.boolean,
            value=value2)

        with self.assertRaises(ValidationError):
            Synonym(source=term1, target=term2).clean()

    @given(
        value1=strategies.booleans(),
        value2=strategies.booleans(),
        metadata=strategies.fixed_dictionaries({
            'prop2': strategies.text(),
        }),
    )
    def test_clean_valid_metadata(self, value1, value2, metadata):
        term1, _ = Term.objects.get_or_create(
            term_type=self.categorical,
            value=value1)
        term2, _ = Term.objects.get_or_create(
            term_type=self.categorical,
            value=value2)
        Synonym(source=term1, target=term2, metadata=metadata).clean()

    @given(
        value1=strategies.booleans(),
        value2=strategies.booleans(),
        metadata=strategies.dictionaries(strategies.text(), strategies.text()),
    )
    def test_clean_invalid_metadata(self, value1, value2, metadata):
        assume('prop2' not in metadata)

        term1, _ = Term.objects.get_or_create(
            term_type=self.categorical,
            value=value1)
        term2, _ = Term.objects.get_or_create(
            term_type=self.categorical,
            value=value2)

        with self.assertRaises(ValidationError):
            Synonym(source=term1, target=term2, metadata=metadata).clean()
