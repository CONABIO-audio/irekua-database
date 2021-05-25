import pytest

from irekua_schemas.models import Schema


@pytest.fixture
@pytest.mark.django_db
def schema_factory():
    def create_schema(
        name,
        schema,
        description=None,
    ):
        if description is None:
            description = f"Schema {name}"

        return Schema.objects.create(
            name=name,
            description=description,
            schema=schema,
        )

    return create_schema


@pytest.fixture
@pytest.mark.django_db
def trivial_schema(schema_factory):
    return schema_factory(
        name="trivial schema",
        schema={
            "$id": "http://irekua.com/null.json",
            "type": "null",
            "title": "Null schema",
            "$schema": "http://json-schema.org/draft-07/schema#",
        },
    )


{
    "$id": "http://irekua.com/object.json",
    "type": "object",
    "title": "Object schema",
    "$schema": "http://json-schema.org/draft-07/schema#",
    "required": [],
    "properties": {},
    "definitions": {},
}


@pytest.fixture
@pytest.mark.django_db
def object_schema(schema_factory):
    return schema_factory(
        name="object schema",
        schema={
            "$id": "http://irekua.com/object.json",
            "type": "object",
            "title": "Object schema",
            "$schema": "http://json-schema.org/draft-07/schema#",
            "required": [],
            "properties": {},
            "definitions": {},
        },
    )


@pytest.fixture
@pytest.mark.django_db
def empty_object_schema(schema_factory):
    return schema_factory(
        name="empty object schema",
        schema={
            "$id": "http://irekua.com/strict_null.json",
            "type": "object",
            "title": "Empty object schema",
            "$schema": "http://json-schema.org/draft-07/schema#",
            "required": [],
            "properties": {},
            "definitions": {},
            "additionalProperties": False,
        },
    )


@pytest.fixture
@pytest.mark.django_db
def string_schema(schema_factory):
    return schema_factory(
        name="string schema",
        schema={
            "$id": "http://irekua.com/string.json",
            "type": "string",
            "title": "String schema",
            "$schema": "http://json-schema.org/draft-07/schema#",
        },
    )


@pytest.fixture
@pytest.mark.django_db
def integer_schema(schema_factory):
    return schema_factory(
        name="integer schema",
        schema={
            "$id": "http://irekua.com/integer.json",
            "type": "integer",
            "title": "Integer schema",
            "$schema": "http://json-schema.org/draft-07/schema#",
        },
    )


@pytest.fixture
@pytest.mark.django_db
def number_schema(schema_factory):
    return schema_factory(
        name="number schema",
        schema={
            "$id": "http://irekua.com/number.json",
            "type": "number",
            "title": "Number schema",
            "$schema": "http://json-schema.org/draft-07/schema#",
        },
    )


@pytest.fixture
@pytest.mark.django_db
def boolean_schema(schema_factory):
    return schema_factory(
        name="boolean schema",
        schema={
            "$id": "http://irekua.com/boolean.json",
            "type": "boolean",
            "title": "Boolean schema",
            "$schema": "http://json-schema.org/draft-07/schema#",
        },
    )


@pytest.fixture
@pytest.mark.django_db
def integer_array_schema(schema_factory):
    return schema_factory(
        name="integer array schema",
        schema={
            "$id": "http://irekua.com/integer_array.json",
            "type": "array",
            "title": "Integer Array schema",
            "items": {"type": "integer"},
            "$schema": "http://json-schema.org/draft-07/schema#",
        },
    )


@pytest.fixture
@pytest.mark.django_db
def example_schema(schema_factory):
    return schema_factory(
        name="example schema",
        schema={
            "$schema": "http://json-schema.org/draft-07/schema",
            "$id": "http://example.com/root.json",
            "type": "object",
            "title": "The Root Schema",
            "description": "The root schema is the schema that comprises the entire JSON document.",
            "default": {},
            "required": [
                "checked",
                "dimensions",
                "id",
                "name",
                "price",
                "tags",
            ],
            "properties": {
                "checked": {
                    "$id": "#/properties/checked",
                    "type": "boolean",
                    "title": "The Checked Schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": False,
                    "examples": [False],
                },
                "dimensions": {
                    "$id": "#/properties/dimensions",
                    "type": "object",
                    "title": "The Dimensions Schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": {},
                    "examples": [{"height": 10.0, "width": 5.0}],
                    "required": ["width", "height"],
                    "properties": {
                        "width": {
                            "$id": "#/properties/dimensions/properties/width",
                            "type": "integer",
                            "title": "The Width Schema",
                            "description": "An explanation about the purpose of this instance.",
                            "default": 0,
                            "examples": [5],
                        },
                        "height": {
                            "$id": "#/properties/dimensions/properties/height",
                            "type": "integer",
                            "title": "The Height Schema",
                            "description": "An explanation about the purpose of this instance.",
                            "default": 0,
                            "examples": [10],
                        },
                    },
                },
                "id": {
                    "$id": "#/properties/id",
                    "type": "integer",
                    "title": "The Id Schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": 0,
                    "examples": [1],
                },
                "name": {
                    "$id": "#/properties/name",
                    "type": "string",
                    "title": "The Name Schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": "",
                    "examples": ["A green door"],
                },
                "price": {
                    "$id": "#/properties/price",
                    "type": "number",
                    "title": "The Price Schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": 0,
                    "examples": [12.5],
                },
                "tags": {
                    "$id": "#/properties/tags",
                    "type": "array",
                    "title": "The Tags Schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": [],
                    "examples": [["home", "green"]],
                    "items": {
                        "$id": "#/properties/tags/items",
                        "type": "string",
                        "title": "The Items Schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": "",
                        "examples": ["home", "green"],
                    },
                },
            },
        },
    )
