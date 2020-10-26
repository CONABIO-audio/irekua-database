import os
import importlib.util

from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase


class MediaInfoExtractor(IrekuaModelBase):
    media_info_type = models.OneToOneField(
        'MediaInfoType',
        models.CASCADE,
        db_column='media_info_type_id',
        verbose_name=_('media info type'),
        help_text=_('Media info type that can be extracted by this extractor'))

    python_file = models.FileField(
        upload_to='media_info_extractors/',
        db_column='python_file',
        verbose_name=_('python file'),
        help_text=_('Python file containing the media info extractor function'),
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Media Info Extractor')

        verbose_name_plural = _('Media Info Extractors')

        ordering = ['-created_on']

    def __str__(self):
        return str(self.media_info_type)

    def load_extractor(self):
        name = self.python_file.name
        basename = os.path.basename(name)
        module_name = os.path.splitext(basename)[0]

        spec = importlib.util.spec_from_file_location(
            module_name,
            self.python_file.path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module.extract

    def extract_media_info(self, fileobj):
        extractor = self.load_extractor()
        return extractor(fileobj)
