from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from irekua_database.base import IrekuaModelBase
from irekua_schemas.utils import validate_JSON_schema
from irekua_schemas.utils import validate_JSON_instance


class Schema(IrekuaModelBase):
    name = models.CharField(
        max_length=256,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name of schema'),
        unique=True,
        blank=False)

    description = models.TextField(
        blank=True,
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Schema description'))

    schema = models.JSONField(
        db_column='schema',
        verbose_name=_('schema'),
        help_text=_('JSON Schema'),
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Schema')
        verbose_name_plural = _('Schemata')

        ordering = [
            '-created_on',
        ]

    def __str__(self):
        return str(self.name)

    def clean(self):
        super().clean()

        try:
            validate_JSON_schema(self.schema)

        except ValidationError as error:
            msg = _(
                'Not a valid JSON schema.'
                'Error: %(error)s')
            params = dict(error=', '.join(error.messages))
            raise ValidationError({'schema': msg % params}) from error

    def is_valid(self, instance):
        try:
            self.validate(instance)
            return True
        except ValidationError:
            return False

    def validate(self, instance):
        try:
            validate_JSON_instance(
                schema=self.schema,
                instance=instance)
        except ValidationError as error:
            msg = _(
                'JSON does not comply with the schema %(schema)s. '
                'Error: %(error)s')
            params = dict(
                schema=self,
                error=', '.join(error.messages))
            raise ValidationError(msg, params=params)
