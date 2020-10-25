from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase
from irekua_annotations.models import Annotation


class AnnotationAnnotator(IrekuaModelBase):
    annotation = models.OneToOneField(
        Annotation,
        on_delete=models.CASCADE,
        db_column='annotation_id',
        verbose_name=_('annotation'),
        help_text=_(
            'Annotation that was created with this '
            ' annotator.'),
        blank=False,
        null=False)

    annotator_version = models.ForeignKey(
        'AnnotatorVersion',
        on_delete=models.PROTECT,
        db_column='annotator_version_id',
        verbose_name=_('annotator version'),
        help_text=_('Annotator version used to create this annotation'),
        blank=False,
        null=False)

    annotator_configuration = models.JSONField(
        db_column='annotator_configuration',
        verbose_name=_('annotator configuration'),
        help_text=_('Configuration of annotator at annotation creation'),
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Annotation Annotator')

        verbose_name_plural = _('Annotation Annotators')

        ordering = ['-created_on']

    def __str__(self):
        return str(self.id)
