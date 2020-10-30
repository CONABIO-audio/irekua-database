from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase
from irekua_schemas.models import Schema


class AnnotatorVersion(IrekuaModelBase):
    annotator = models.ForeignKey(
        'Annotator',
        on_delete=models.CASCADE,
        db_column='annotation_tool_id',
        verbose_name=_('annotation tool'),
        help_text=_('Annotation tool'),
        blank=False,
        null=False)

    version = models.CharField(
        max_length=16,
        db_column='version',
        verbose_name=_('version'),
        help_text=_('Annotator version'),
        blank=False)

    configuration_schema = models.ForeignKey(
        Schema,
        models.PROTECT,
        db_column='configuration_schema',
        verbose_name=_('configuration schema'),
        help_text=_('JSON schema for annotator configuration'),
        null=True,
        blank=True)

    class Meta:
        verbose_name = _('Annotator Version')

        verbose_name_plural = _('Annotator Versions')

        ordering = ['-created_on']

    def __str__(self):
        return f'{self.annotator} @ {self.version}'

    def validate_configuration(self, configuration):
        if self.configuration_schema is None:
            return

        try:
            # pylint: disable=no-member
            self.configuration_schema.validate(configuration)

        except ValidationError as error:
            msg = _(
                'Invalid configuration information for annotator '
                '%(annotator_version)s. Error: %(error)s')
            params = dict(
                annotator_version=self,
                error=error)
            raise ValidationError(msg % params) from error