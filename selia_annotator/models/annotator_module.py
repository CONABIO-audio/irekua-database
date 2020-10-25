import os

from django.db import models
from django.utils.translation import gettext_lazy as _

from .annotator_version import AnnotatorVersion


def annotator_path(instance, filename):
    _, ext = os.path.splitext(filename)
    return 'annotators/{name}_{version}.{ext}'.format(
        name=instance.annotation_tool.name.replace(' ', '_'),
        version=instance.annotation_tool.version.replace('.', '_'),
        ext=ext)


class AnnotatorModule(AnnotatorVersion):
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

    def deactivate(self):
        self.is_active = False
        self.save()

    def save(self, *args, **kwargs):
        if self.is_active:
            queryset = AnnotatorModule.objects.filter(
                annotator__annotation_type=self.annotator.annotation_type,
                is_active=True)

            for entry in queryset:
                if entry != self:
                    entry.deactivate()

        super().save(*args, **kwargs)
