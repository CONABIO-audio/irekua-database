import os

from django.db import models
from django.utils.translation import gettext_lazy as _

from .visualizer_version import VisualizerVersion


def visualizer_version_module_path(instance, filename):
    _, ext = os.path.splitext(filename)
    return 'visualizers/{name}_{version}.{ext}'.format(
        name=instance.visualizer.name.replace(' ', '_'),
        version=instance.visualizer.version.replace('.', '_'),
        ext=ext)


class VisualizerModule(VisualizerVersion):
    javascript_file = models.FileField(
        upload_to=visualizer_version_module_path,
        db_column='javascript_file',
        verbose_name=_('javascript file'),
        help_text=_('Javascript file containing visualizer version module'),
        blank=False,
        null=False)

    is_active = models.BooleanField(
        db_column='is_active',
        verbose_name=_('is active'),
        default=True,
        blank=False,
        null=False,
        help_text=_(
            'Boolean flag that indicates whether this version is '
            'to be used as the default version of this visualizer.'))

    class Meta:
        verbose_name = _('Visualizer Module')

        verbose_name_plural = _('Visualizer Modules')

        ordering = ['-created_on']

    def __str__(self):
        return str(self.visualizer)

    def clean(self):
        super().clean()

        if self.is_active:
            for visualizer in VisualizerModule.objects.filter(visualizer=self.visualizer):
                visualizer.is_active = False
                visualizer.save()

            self.is_active = True
