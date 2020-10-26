import os

from django.db import models
from django.utils.translation import gettext_lazy as _

from sorl.thumbnail import ImageField

from irekua_database.base import IrekuaModelBase


def get_thumbnail_path(instance, filename):
    path_fmt = os.path.join(
        'thumbnails',
        '{hash}{ext}')
    extension = 'jpg'
    hash_string = instance.hash
    return path_fmt.format(hash=hash_string, ext=extension)


class ItemThumbnail(IrekuaModelBase):
    item = models.OneToOneField(
        'Item',
        models.CASCADE,
        primary_key=True,
        db_column='item_id',
        verbose_name=_('item'),
        help_text=_('Item whose thumbnail is this.'))

    thumbnail = ImageField(
        upload_to=get_thumbnail_path,
        db_column='thumbnail',
        verbose_name=_('thumbnail'),
        help_text=_('Thumbnail associated to item'),
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Item Thumbnail')

        verbose_name_plural = _('Items Thumbnails')

        ordering = ['created_on']
