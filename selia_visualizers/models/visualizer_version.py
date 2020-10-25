from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase
from irekua_schemas.models import Schema


class VisualizerVersion(IrekuaModelBase):
    visualizer = models.ForeignKey(
        'Visualizer',
        models.CASCADE,
        db_column='visualizer_id',
        verbose_name=_('visualizer'),
        help_text=_('Visualizer'),
        blank=False,
        null=False)

    version = models.CharField(
        max_length=16,
        db_column='version',
        verbose_name=_('version'),
        help_text=_('Version of visualizer app'),
        blank=False,
        null=False)

    configuration_schema = models.ForeignKey(
        Schema,
        models.PROTECT,
        db_column='configuration_schema_id',
        verbose_name=_('configuration schema'),
        help_text=_('JSON schema for visualizer tool configuration info'),
        null=True,
        blank=True)

    class Meta:
        verbose_name = _('Visualizer Version')

        verbose_name_plural = _('Visualizer Versions')

        ordering = ['visualizer', '-version']

        unique_together = (
            ('visualizer', 'version'),
        )

    def __str__(self):
        return f'{self.visualizer} @ {self.version}'

    def validate_configuration(self, configuration):
        if self.configuration_schema is None:
            return

        try:
            # pylint: disable=no-member
            self.configuration_schema.validate(configuration)

        except ValidationError as error:
            msg = _('Invalid visualizer configuration. Error: %(error)s')
            params = dict(error=error)
            raise ValidationError(msg % params) from error
