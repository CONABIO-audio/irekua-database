import mimetypes
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase
from irekua_schemas.mixins import MetadataSchemaMixin


mimetypes.init()


class ItemType(IrekuaModelBase, MetadataSchemaMixin):
    name = models.CharField(
        max_length=64,
        db_column='name',
        verbose_name=_('name'),
        unique=True,
        help_text=_('Name of item type'),
        blank=False)

    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of item type'),
        blank=False)

    icon = models.ImageField(
        db_column='icon',
        verbose_name=_('icon'),
        help_text=_('Item type icon'),
        upload_to='images/item_types/',
        blank=True,
        null=True)

    mime_types = models.ManyToManyField(
        'MimeType',
        db_column='mime_types',
        verbose_name=_('mime types'),
        help_text=_('Mime types of files for this item type'),
        blank=True)

    media_info_type = models.ForeignKey(
        'MediaInfoType',
        models.PROTECT,
        db_column='media_info_type_id',
        verbose_name=_('media info type'),
        help_text=_('Type of media info associated to items of this type'),
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Item Type')
        verbose_name_plural = _('Item Types')

        ordering = ['name']

    def __str__(self):
        return self.name

    def validate_mime_type(self, mime_type):
        if not self.mime_types.filter(pk=mime_type.pk).exists():
            msg = _(
                'The MIME type %(mime_type)s is not accepted for items '
                'of type %(item_type)s')
            params = dict(
                mime_type=mime_type,
                item_type=self)
            raise ValidationError(msg % params)

    def validate_media_info(self, media_info):
        if self.media_info_type is None:
            return

        try:
            # pylint: disable=no-member
            self.media_info_type.validate_media_info(media_info)

        except ValidationError as error:
            msg = _(
                'Media info is invalid for item of type %(item_type)s. '
                'Error: %(error)s')
            params = dict(
                item_type=self,
                error=error)
            raise  ValidationError(msg % params) from error
