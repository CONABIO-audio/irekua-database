from django.core.exceptions import ValidationError
from hypothesis import given
from hypothesis import strategies
from hypothesis import assume
from hypothesis.extra.django import TestCase

from irekua_schemas.models import Schema

from .strategies import valid_string
from .strategies import random_schema



class SchemaTestCase(TestCase):
    fixtures = ['irekua_schemas/schemas.json']

    def setUp(self):
        self.null = Schema.objects.get(name='null')
        self.object = Schema.objects.get(name='object')
        self.empty = Schema.objects.get(name='empty object')
        self.string = Schema.objects.get(name='string')
        self.integer = Schema.objects.get(name='integer')
        self.number = Schema.objects.get(name='number')
        self.boolean = Schema.objects.get(name='boolean')
        self.array = Schema.objects.get(name='array')
        self.example = Schema.objects.get(name='example')

    def test_null_validate(self):
        self.assertTrue(self.null.is_valid(None))
        self.assertFalse(self.object.is_valid(None))
        self.assertFalse(self.empty.is_valid(None))
        self.assertFalse(self.string.is_valid(None))
        self.assertFalse(self.integer.is_valid(None))
        self.assertFalse(self.number.is_valid(None))
        self.assertFalse(self.boolean.is_valid(None))
        self.assertFalse(self.array.is_valid(None))
        self.assertFalse(self.example.is_valid(None))

    @given(strategies.text())
    def test_string_validate(self, t):
        self.assertFalse(self.null.is_valid(t))
        self.assertFalse(self.object.is_valid(t))
        self.assertFalse(self.empty.is_valid(t))
        self.assertTrue(self.string.is_valid(t))
        self.assertFalse(self.integer.is_valid(t))
        self.assertFalse(self.number.is_valid(t))
        self.assertFalse(self.boolean.is_valid(t))
        self.assertFalse(self.array.is_valid(t))
        self.assertFalse(self.example.is_valid(t))

    @given(strategies.booleans())
    def test_boolean_validate(self, t):
        self.assertFalse(self.null.is_valid(t))
        self.assertFalse(self.object.is_valid(t))
        self.assertFalse(self.empty.is_valid(t))
        self.assertFalse(self.string.is_valid(t))
        self.assertFalse(self.integer.is_valid(t))
        self.assertFalse(self.number.is_valid(t))
        self.assertTrue(self.boolean.is_valid(t))
        self.assertFalse(self.array.is_valid(t))
        self.assertFalse(self.example.is_valid(t))

    @given(strategies.floats())
    def test_float_validate(self, t):
        self.assertFalse(self.null.is_valid(t))
        self.assertFalse(self.object.is_valid(t))
        self.assertFalse(self.empty.is_valid(t))
        self.assertFalse(self.string.is_valid(t))
        self.assertTrue(self.number.is_valid(t))
        self.assertFalse(self.boolean.is_valid(t))
        self.assertFalse(self.array.is_valid(t))
        self.assertFalse(self.example.is_valid(t))

        if t % 1 != 0:
            self.assertFalse(self.integer.is_valid(t))
        else:
            self.assertTrue(self.integer.is_valid(t))

    @given(strategies.integers())
    def test_integers_validate(self, t):
        self.assertFalse(self.null.is_valid(t))
        self.assertFalse(self.object.is_valid(t))
        self.assertFalse(self.empty.is_valid(t))
        self.assertFalse(self.string.is_valid(t))
        self.assertTrue(self.integer.is_valid(t))
        self.assertTrue(self.number.is_valid(t))
        self.assertFalse(self.boolean.is_valid(t))
        self.assertFalse(self.array.is_valid(t))
        self.assertFalse(self.example.is_valid(t))

    @given(strategies.lists(strategies.integers()))
    def test_list_validate(self, t):
        self.assertFalse(self.null.is_valid(t))
        self.assertFalse(self.object.is_valid(t))
        self.assertFalse(self.empty.is_valid(t))
        self.assertFalse(self.string.is_valid(t))
        self.assertFalse(self.integer.is_valid(t))
        self.assertFalse(self.number.is_valid(t))
        self.assertFalse(self.boolean.is_valid(t))
        self.assertTrue(self.array.is_valid(t))
        self.assertFalse(self.example.is_valid(t))

    def test_empty_validate(self):
        self.assertFalse(self.null.is_valid({}))
        self.assertTrue(self.object.is_valid({}))
        self.assertTrue(self.empty.is_valid({}))
        self.assertFalse(self.string.is_valid({}))
        self.assertFalse(self.integer.is_valid({}))
        self.assertFalse(self.number.is_valid({}))
        self.assertFalse(self.boolean.is_valid({}))
        self.assertFalse(self.array.is_valid({}))
        self.assertFalse(self.example.is_valid({}))

    @given(strategies.dictionaries(strategies.text(), strategies.text()))
    def test_object_validate(self, t):
        self.assertFalse(self.null.is_valid(t))
        self.assertTrue(self.object.is_valid(t))
        self.assertFalse(self.string.is_valid(t))
        self.assertFalse(self.integer.is_valid(t))
        self.assertFalse(self.number.is_valid(t))
        self.assertFalse(self.boolean.is_valid(t))
        self.assertFalse(self.array.is_valid(t))
        self.assertFalse(self.example.is_valid(t))

        if t:
            self.assertFalse(self.empty.is_valid(t))
        else:
            self.assertTrue(self.empty.is_valid(t))

    @given(strategies.fixed_dictionaries({
        'checked': strategies.booleans(),
        'dimensions': strategies.fixed_dictionaries({
            'width': strategies.integers(),
            'height': strategies.integers(),
        }),
        'id': strategies.integers(),
        'name': strategies.text(),
        'price': strategies.floats(),
        'tags': strategies.lists(strategies.text()),
    }))
    def test_example_validate(self, t):
        self.assertFalse(self.null.is_valid(t))
        self.assertTrue(self.object.is_valid(t))
        self.assertFalse(self.empty.is_valid(t))
        self.assertFalse(self.string.is_valid(t))
        self.assertFalse(self.integer.is_valid(t))
        self.assertFalse(self.number.is_valid(t))
        self.assertFalse(self.boolean.is_valid(t))
        self.assertFalse(self.array.is_valid(t))
        self.assertTrue(self.example.is_valid(t))

    @given(
        name=valid_string(5),
        description=valid_string(20),
        schema=strategies.dictionaries(valid_string(1), valid_string(2)),
    )
    def test_validate_json_schema_invalid_schema(self, name, description, schema):
        assume(len(schema) != 0)

        with self.assertRaises(ValidationError):
            schema = Schema(
                name=name,
                description=description,
                schema=schema)

            schema.clean()
            schema.save()

    @given(
        name=valid_string(5),
        description=valid_string(20),
        schema=random_schema(),
    )
    def test_validate_json_schema_valid_schema(self, name, description, schema):
        schema = Schema(
            name=name,
            description=description,
            schema=schema)

        schema.clean()
        schema.save()
