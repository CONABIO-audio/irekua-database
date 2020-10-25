import os

from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase


def visualizer_version_module_path(instance, filename):
    version = instance.visualizer_version
    _, ext = os.path.splitext(filename)
    return 'visualizers/{name}_{version}.{ext}'.format(
        name=version.visualizer.name.replace(' ', '_'),
        version=version.version.replace('.', '_'),
        ext=ext)


class VisualizerModule(IrekuaModelBase):
    visualizer_version = models.OneToOneField(
        'VisualizerVersion',
        on_delete=models.CASCADE,
        db_column='visualizer_version_id',
        verbose_name=_('visualizer version'),
        help_text=_('visualizer version to which this module belongs'),
        blank=False,
        null=False)

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

    def _deactivate_others(self):
        # pylint: disable=no-member
        visualizer = self.visualizer_version.visualizer
        (
            VisualizerModule.objects
            .filter(
                visualizer_version__visualizer=visualizer,
                is_active=True
            )
            .exclude(pk=self.pk)
            .update(is_active=False)
        )

    # pylint: disable=signature-differs
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.is_active:
            self._deactivate_others()
