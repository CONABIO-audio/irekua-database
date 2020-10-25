from django.db import models
from django.core.exceptions import ValidationError
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
        null=True)

    class Meta:
        verbose_name = _('Annotation Visualizer')

        verbose_name_plural = _('Annotation Visualizers')

        ordering = ['-created_on']

    def clean(self):
        super().clean()

        # Check that configuration data is valid for visualizer version
        self.clean_configuration()

        # Check that item type can be visualized with visualizer
        self.clean_compatible_item_type()

    def clean_configuration(self):
        try:
            # pylint: disable=no-member
            self.visualizer_version.validate_configuration(self.visualizer_configuration)

        except ValidationError as error:
            raise ValidationError({'visualizer_configuration': error}) from error

    def clean_compatible_item_type(self):
        # pylint: disable=no-member
        item_type = self.annotation.item.item_type
        visualizer = self.visualizer_version.visualizer

        try:
            visualizer.validate_item_type(item_type)

        except ValidationError as error:
            raise ValidationError({'visualizer_version': error}) from error
