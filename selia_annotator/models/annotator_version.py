from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase


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

    class Meta:
        verbose_name = _('Annotator Version')

        verbose_name_plural = _('Annotator Versions')

        ordering = ['-created_on']

    def __str__(self):
        return f'{self.annotator.name} @ {self.version}'
