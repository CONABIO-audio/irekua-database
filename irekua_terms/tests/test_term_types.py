from django.core.exceptions import ValidationError
from hypothesis import given
from hypothesis import strategies
from hypothesis import assume
from hypothesis.extra.django import TestCase

from irekua_schemas.models import Schema
from irekua_terms.models import TermType


def _string_is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


valid_string = lambda: strategies.text(
    alphabet=strategies.characters(
        blacklist_categories=("Cs", "Cc"),
    ),
    min_size=5,
)


class TermTypeTestCase(TestCase):
    fixtures = [
        "irekua_terms/categorical.json",
        "irekua_terms/numeric.json",
        "irekua_terms/integer.json",
        "irekua_terms/boolean.json",
    ]

    def setUp(self):
        self.cat1 = TermType.objects.get(name="categorical1")
        self.cat2 = TermType.objects.get(name="categorical2")
        self.cat_no_meta = TermType.objects.get(name="categorical_no_metadata")
        self.numeric = TermType.objects.get(name="numeric")
        self.integer = TermType.objects.get(name="integer")
        self.boolean = TermType.objects.get(name="boolean")
        self.metadata_schema = Schema.objects.get(name="categorical_metadata")
        self.synonym_schema = Schema.objects.get(name="synonym_metadata")

    @given(strategies.text(min_size=3))
    def test_validate_string_values(self, value):
        assume(not _string_is_number(value))

        self.cat1.validate_value(value)

        with self.assertRaises(ValidationError):
            self.boolean.validate_value(value)

        with self.assertRaises(ValidationError):
            self.integer.validate_value(value)

        with self.assertRaises(ValidationError):
            self.numeric.validate_value(value)

    @given(strategies.floats())
    def test_validate_numerical_values(self, value):
        assume(value % 1 != 0)

        self.numeric.validate_value(value)
        self.numeric.validate_value(str(value))

        with self.assertRaises(ValidationError):
            self.boolean.validate_value(value)

        with self.assertRaises(ValidationError):
            self.boolean.validate_value(str(value))

        with self.assertRaises(ValidationError):
            self.integer.validate_value(value)

        with self.assertRaises(ValidationError):
            self.integer.validate_value(str(value))

        with self.assertRaises(ValidationError):
            self.cat1.validate_value(value)
        self.cat1.validate_value(str(value))

    @given(strategies.integers())
    def test_validate_integer_values(self, value):
        assume(value not in [0, 1])

        self.integer.validate_value(value)
        self.integer.validate_value(str(value))

        with self.assertRaises(ValidationError):
            self.boolean.validate_value(value)

        with self.assertRaises(ValidationError):
            self.boolean.validate_value(str(value))

        self.numeric.validate_value(value)
        self.numeric.validate_value(str(value))

        with self.assertRaises(ValidationError):
            self.cat1.validate_value(value)
        self.cat1.validate_value(str(value))

    @given(strategies.booleans())
    def test_validate_boolean_values(self, value):
        self.boolean.validate_value(value)
        self.boolean.validate_value(str(value))

        with self.assertRaises(ValidationError):
            self.numeric.validate_value(value)

        with self.assertRaises(ValidationError):
            self.numeric.validate_value(str(value))

        with self.assertRaises(ValidationError):
            self.integer.validate_value(value)

        with self.assertRaises(ValidationError):
            self.integer.validate_value(str(value))

        with self.assertRaises(ValidationError):
            self.cat1.validate_value(value)
        self.cat1.validate_value(str(value))

    @given(strategies.dictionaries(strategies.text(), strategies.text()))
    def test_validate_invalid_metadata(self, metadata):
        assume("prop1" not in metadata)

        with self.assertRaises(ValidationError):
            self.cat1.validate_metadata(metadata)

        self.cat_no_meta.validate_metadata(metadata)

    @given(strategies.fixed_dictionaries({"prop1": strategies.text()}))
    def test_validate_valid_metadata(self, metadata):
        self.cat1.validate_metadata(metadata)
        self.cat_no_meta.validate_metadata(metadata)

    @given(strategies.dictionaries(strategies.text(), strategies.text()))
    def test_validate_invalid_synonym_metadata(self, metadata):
        assume("prop2" not in metadata)

        with self.assertRaises(ValidationError):
            self.cat1.validate_synonym_metadata(metadata)

        with self.assertRaises(ValidationError):
            self.cat_no_meta.validate_synonym_metadata(metadata)

        with self.assertRaises(ValidationError) as error:
            self.numeric.validate_synonym_metadata(metadata)
            self.assertTrue("type does not support synonyms" in error.message)

        with self.assertRaises(ValidationError) as error:
            self.integer.validate_synonym_metadata(metadata)
            self.assertTrue("type does not support synonyms" in error.message)

        with self.assertRaises(ValidationError) as error:
            self.boolean.validate_synonym_metadata(metadata)
            self.assertTrue("type does not support synonyms" in error.message)

    @given(
        strategies.fixed_dictionaries(
            {
                "prop2": strategies.text(),
            }
        )
    )
    def test_validate_valid_synonym_metadata(self, metadata):
        self.cat1.validate_synonym_metadata(metadata)

        with self.assertRaises(ValidationError):
            self.cat_no_meta.validate_synonym_metadata(metadata)

        with self.assertRaises(ValidationError) as error:
            self.numeric.validate_synonym_metadata(metadata)
            self.assertTrue("type does not support synonyms" in error.message)

        with self.assertRaises(ValidationError) as error:
            self.integer.validate_synonym_metadata(metadata)
            self.assertTrue("type does not support synonyms" in error.message)

        with self.assertRaises(ValidationError) as error:
            self.boolean.validate_synonym_metadata(metadata)
            self.assertTrue("type does not support synonyms" in error.message)

    def test_clean(self):
        term_categorical = TermType(
            name="test",
            description="Testing term",
            metadata_schema=self.metadata_schema,
            synonym_metadata_schema=self.synonym_schema,
            is_categorical=True,
            is_numerical=False,
            is_integer=False,
            is_boolean=False,
        )
        term_categorical.clean()

        term_no_schema = TermType(
            name="test_no_meta",
            description="Testing term with no schemas",
            metadata_schema=None,
            synonym_metadata_schema=None,
            is_categorical=True,
            is_numerical=False,
            is_integer=False,
            is_boolean=False,
        )
        term_no_schema.clean()

    @given(
        is_categorical=strategies.booleans(),
        is_numerical=strategies.booleans(),
        is_integer=strategies.booleans(),
        is_boolean=strategies.booleans(),
    )
    def test_clean_only_one_type(
        self, is_categorical, is_numerical, is_integer, is_boolean
    ):
        boolean_sum = is_categorical + is_numerical + is_integer + is_boolean

        term = TermType(
            name="test",
            description="Testing term",
            metadata_schema=None,
            synonym_metadata_schema=None,
            is_categorical=is_categorical,
            is_numerical=is_numerical,
            is_integer=is_integer,
            is_boolean=is_boolean,
        )

        if boolean_sum != 1:
            with self.assertRaises(ValidationError):
                term.clean()
        else:
            term.clean()

    @given(
        name=valid_string(),
        description=valid_string(),
    )
    def test_clean_no_synonym_metadata(self, name, description):
        TermType(
            name=name,
            description=description,
            is_categorical=False,
            is_numerical=True,
            is_integer=False,
            is_boolean=False,
            metadata_schema=None,
            synonym_metadata_schema=None,
        ).clean()
        with self.assertRaises(ValidationError):
            TermType(
                name=name,
                description=description,
                is_categorical=False,
                is_numerical=True,
                is_integer=False,
                is_boolean=False,
                metadata_schema=None,
                synonym_metadata_schema=self.synonym_schema,
            ).clean()

        TermType(
            name=name,
            description=description,
            is_categorical=False,
            is_numerical=False,
            is_integer=True,
            is_boolean=False,
            metadata_schema=None,
            synonym_metadata_schema=None,
        ).clean()
        with self.assertRaises(ValidationError):
            TermType(
                name=name,
                description=description,
                is_categorical=False,
                is_numerical=False,
                is_integer=True,
                is_boolean=False,
                metadata_schema=None,
                synonym_metadata_schema=self.synonym_schema,
            ).clean()

        TermType(
            name=name,
            description=description,
            is_categorical=False,
            is_numerical=False,
            is_integer=False,
            is_boolean=True,
            metadata_schema=None,
            synonym_metadata_schema=None,
        ).clean()
        with self.assertRaises(ValidationError):
            TermType(
                name=name,
                description=description,
                is_categorical=False,
                is_numerical=True,
                is_integer=False,
                is_boolean=True,
                metadata_schema=None,
                synonym_metadata_schema=self.synonym_schema,
            ).clean()
