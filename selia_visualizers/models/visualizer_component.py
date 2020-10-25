import os

from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_items.models import ItemType


def visualizer_path(instance, filename):
    _, ext = os.path.splitext(filename)
    return 'visualizers/{name}_{version}.{ext}'.format(
        name=instance.visualizer.name.replace(' ', '_'),
        version=instance.visualizer.version.replace('.', '_'),
        ext=ext)


class VisualizerComponent(models.Model):
    visualizer = models.OneToOneField(
        'Visualizer',
        on_delete=models.CASCADE,
        db_column='visualizer_id',
        verbose_name=_('visualizer'),
        help_text=_('Visualizer'),
        blank=False,
        null=False)

    javascript_file = models.FileField(
        upload_to=visualizer_path,
        db_column='javascript_file',
        verbose_name=_('javascript file'),
        help_text=_('Javascript file containing visualizer component'),
        blank=False,
        null=False)

    item_types = models.ManyToManyField(
        ItemType,
        through='VisualizerComponentItemType',
        through_fields=('visualizer_component', 'item_type'))

    class Meta:
        verbose_name = _('Visualizer Component')
        verbose_name_plural = _('Visualizers Components')

    def __str__(self):
        return str(self.visualizer)
