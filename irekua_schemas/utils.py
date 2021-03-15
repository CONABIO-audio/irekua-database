import jsonschema

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def validate_JSON_schema(schema):
    if schema is None:
        raise ValidationError(_("Invalid JSON"))

    if "type" not in schema:
        msg = _("JSON Schema is not valid, no type field.")
        raise ValidationError(msg)

    try:
        jsonschema.validate(instance={}, schema=schema)

    except jsonschema.exceptions.SchemaError as error:
        msg = _("JSON Schema is not valid. Error: %(error)s")
        params = dict(error=error.message)
        raise ValidationError(msg, params=params) from error

    except jsonschema.exceptions.ValidationError:
        pass


def validate_JSON_instance(schema=None, instance=None):
    try:
        jsonschema.validate(instance=instance, schema=schema)

    except jsonschema.exceptions.ValidationError as error:
        raise ValidationError(error.message) from error
