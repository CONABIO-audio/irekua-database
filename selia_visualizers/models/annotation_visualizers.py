from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase
from irekua_annotations.models import Annotation


class AnnotationVisualizer(IrekuaModelBase):
    annotation = models.OneToOneField(
        Annotation,
        on_delete=models.CASCADE,
        db_column='annotation_id',
        verbose_name=_('annotation'),
        help_text=_('Annotation that was created using this visualizer'))

    visualizer_version = models.ForeignKey(
        'VisualizerVersion',
        on_delete=models.CASCADE,
        db_column='visualizer_version_id',
        verbose_name=_('visualizer version'),
        help_text=_('Visualizer version used to create this annotation'))

    visualizer_configuration = models.JSONField(
        db_column='visualizer_configuration',
        verbose_name=_('visualizer configuration'),
        help_text=_('Configuration of visualizer at annotation creation'),
        blank=True,
        null=False)

    class Meta:
        verbose_name = _('Annotation Visualizer')

        verbose_name_plural = _('Annotation Visualizers')

        ordering = ['-created_on']
