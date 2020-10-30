import os

from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase


def annotator_path(instance, filename):
    version = instance.annotator_version
    _, ext = os.path.splitext(filename)
    return 'annotators/{name}_{version}.{ext}'.format(
        name=version.annotator.name.replace(' ', '_'),
        version=version.version.replace('.', '_'),
        ext=ext)


class AnnotatorModule(IrekuaModelBase):
    annotator_version = models.OneToOneField(
        'AnnotatorVersion',
        on_delete=models.CASCADE,
        db_column='annotator_version_id',
        verbose_name=_('annotator version'),
        help_text=_('annotator version to which this module belongs'),
        blank=False,
        null=False)

    javascript_file = models.FileField(
        upload_to=annotator_path,
        db_column='javascript_file',
        verbose_name=_('javascript file'),
        help_text=_('Javascript file containing annotator module'),
        blank=False,
        null=False)

    is_active = models.BooleanField(
        db_column='is_active',
        verbose_name=_('is active'),
        help_text=_(
            'Is this module to be used as default annotator for the '
            'associated annotation type?'),
        default=True,
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Annotator Module')

        verbose_name_plural = _('Annotator Modules')

        ordering = ['-created_on']

    # pylint: disable=signature-differs
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.is_active:
            self._deactivate_others()

    def _deactivate_others(self):
        # pylint: disable=no-member
        annotation_type = self.annotator_version.annotator.annotation_type
        (
            AnnotatorModule.objects
            .filter(
                annotator_version__annotator__annotation_type=annotation_type,
                is_active=True
            )
            .exclude(pk=self.pk)
            .update(is_active=False)
        )
