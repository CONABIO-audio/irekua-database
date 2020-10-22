import mimetypes
import os

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.utils import hash_file
from irekua_database.base import IrekuaModelBase
from irekua_devices.models import MimeType


mimetypes.init()


def get_item_path(instance, filename):
    path_fmt = os.path.join(
        'secondary_items',
        '{collection}',
        '{sampling_event}',
        '{sampling_event_device}',
        '{hash}',
        '{secondary_hash}{ext}')

    extension = mimetypes.guess_extension(
        instance.item_type.media_type)
    item = instance.item
    sampling_event_device = item.sampling_event_device
    sampling_event = sampling_event_device.sampling_event
    collection = sampling_event.collection

    instance.item_file.open()
    hash_string = hash_file(instance.item_file)

    path = path_fmt.format(
        collection=collection.pk,
        sampling_event=sampling_event.pk,
        sampling_event_device=sampling_event_device.pk,
        hash=item.hash,
        secondary_hash=hash_string,
        ext=extension)
    return path


class SecondaryItem(IrekuaModelBase):
    hash = models.CharField(
        max_length=64,
        unique=True,
        db_column='hash',
        verbose_name=_('hash'),
        help_text=_('Hash of secondary resource file'),
        blank=False)

    item_file = models.FileField(
        upload_to=get_item_path,
        db_column='item_file',
        verbose_name=_('item file'),
        help_text=_('Upload file associated to file'),
        blank=True,
        null=True)

    item_type = models.ForeignKey(
        'ItemType',
        on_delete=models.PROTECT,
        db_column='item_type',
        verbose_name=_('item type'),
        help_text=_('Type of file of secondary item'),
        blank=False,
        null=False)

    item = models.ForeignKey(
        'Item',
        db_column='item_id',
        verbose_name=_('item id'),
        help_text=_('Reference to primary item associated to secondary item'),
        on_delete=models.CASCADE,
        blank=False,
        null=False)

    media_info = models.JSONField(
        db_column='media_info',
        verbose_name=_('media info'),
        help_text=_('Media information of secondary item file'),
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Secondary Item')

        verbose_name_plural = _('Secondary Items')

        ordering = ['created_on']

    def __str__(self):
        msg = _('%(itemid)s => %(id)s ')
        params = dict(id=self.id, itemid=str(self.item))
        return msg % params

    def clean(self):
        super().clean()

        # Check that declared hash coincides with uploaded file.
        self.clean_hash()

        # Check that MIME type is declared in the database
        mime_type = self.clean_mime_type()

        # Check that MIME type is valid for item type
        self.clean_compatible_mime_and_item_type(mime_type)

        # Check that media info is valid for MIME type
        self.clean_media_info(mime_type)

    def clean_hash(self):
        try:
            self.validate_hash()

        except ValidationError as error:
            raise ValidationError({'hash': error}) from error

    def clean_mime_type(self):
        try:
            return MimeType.infer(file=self.item_file)

        except MimeType.DoesNotExist as error:
            msg = _(
                'No MIME type could be infered or not registered')
            raise ValidationError({'item_file': msg}) from error

    def clean_compatible_mime_and_item_type(self, mime_type):
        try:
            # pylint: disable=no-member
            self.item_type.validate_mime_type(mime_type)

        except ValidationError as error:
            raise ValidationError({'item_file': error}) from error

    def clean_media_info(self, mime_type):
        try:
            # pylint: disable=no-member
            mime_type.validate_media_info(self.media_info)

        except ValidationError as error:
            raise ValidationError({'media_info': error}) from error

    def validate_hash(self):
        # pylint: disable=no-member
        if self.item_file.name is None and self.hash is None:
            msg = _('If no file is provided, a hash must be given')
            raise ValidationError(msg)

        # pylint: disable=no-member
        if self.item_file.name is None:
            return

        self.item_file.open()
        hash_string = hash_file(self.item_file)

        if self.hash is None:
            self.hash = hash_string

        if self.hash != hash_string:
            msg = _('Hash of file and recorded hash do not coincide')
            raise ValidationError(msg)
