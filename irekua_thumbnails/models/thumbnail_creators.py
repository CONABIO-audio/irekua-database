import os
import importlib.util

from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase
from irekua_items.models import ItemType


class ThumbnailCreator(IrekuaModelBase):
    name = models.CharField(
        max_length=64,
        db_column='name',
        verbose_name=_('name'),
        unique=True,
        help_text=_('Name of thumbnail creator'),
        blank=False)

    python_file = models.FileField(
        upload_to='thumbnail_creators/',
        db_column='python_file',
        verbose_name=_('python file'),
        help_text=_('Python file containing the thumbnail creator function'),
        blank=False,
        null=False)

    item_types = models.ManyToManyField(
        ItemType,
        through='ThumbnailCreatorItemType',
        through_fields=('thumbnail_creator', 'item_type'),
        verbose_name=_('item types'),
        help_text=_('Item types that can be processed by this thumbnail creator'))

    class Meta:
        verbose_name = _('Thumbnail creator')

        verbose_name_plural = _('Thumbnail creators')

        ordering = ['-created_on']

    def __str__(self):
        return self.name

    def load_creator(self):
        name = self.python_file.name
        basename = os.path.basename(name)
        module_name = os.path.splitext(basename)[0]

        spec = importlib.util.spec_from_file_location(
            module_name,
            self.python_file.path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module.creator
