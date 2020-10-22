import os
import mimetypes

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from pytz import timezone as pytz_timezone

from irekua_database.base import IrekuaModelBaseUser
from irekua_database.utils import hash_file
from irekua_devices.models import MimeType


mimetypes.init()


def infer_datetime(
        year=None,
        month=None,
        day=None,
        hour=None,
        minute=None,
        second=None,
        tz_info=None,
        dt=None):
    """
    Infer datetime object from partial information.

    This function can be used to reconstruct the item's captured_on datetime field.
    The inference can be based on a known datetime and replace the datetime attributes
    with the provided information. This is based on the assumption that the date-time
    partial fields (year, hour, etc..) are more reliable than the single datetime field.
    """
    if (year is None) or (month is None) or (day is None):
        msg = _('Year, month and day have to be provided')
        raise ValueError(msg)

    if tz_info is None:
        tz = timezone.get_default_timezone()
    else:
        tz = pytz_timezone(tz_info)

    if dt is None:
        dt = timezone.localtime(timezone=tz).replace(hour=0, minute=0, second=0)
    else:
        dt = timezone.localtime(dt, timezone=tz)

    dt = dt.replace(year=year, month=month, day=day)

    if hour is None:
        return dt

    dt = dt.replace(hour=hour)

    if minute is  None:
        return dt

    dt = dt.replace(minute=minute)

    if second is None:
        return dt

    return dt.replace(second=second)


def get_item_path(instance, filename):
    path_fmt = os.path.join(
        'items',
        '{collection}',
        '{sampling_event}',
        '{sampling_event_device}',
        '{hash}{ext}')

    mime_type, _ = mimetypes.guess_type(filename)
    extension = mimetypes.guess_extension(mime_type)

    sampling_event_device = instance.sampling_event_device
    sampling_event = sampling_event_device.sampling_event
    collection = sampling_event.collection

    instance.item_file.open()
    hash_string = hash_file(instance.item_file)

    path = path_fmt.format(
        collection=collection.pk,
        sampling_event=sampling_event.pk,
        sampling_event_device=sampling_event_device.pk,
        hash=hash_string,
        ext=extension)
    return path


class Item(IrekuaModelBaseUser):
    hash_string = None
    item_size = None

    filesize = models.IntegerField(
        db_column='filesize',
        verbose_name=_('file size'),
        help_text=_('Size of resource in bytes'),
        blank=True,
        null=True)

    hash = models.CharField(
        db_column='hash',
        verbose_name=_('hash'),
        help_text=_('Hash of resource file'),
        max_length=64,
        unique=True,
        blank=True,
        null=False)

    item_type = models.ForeignKey(
        'ItemType',
        on_delete=models.PROTECT,
        db_column='item_type_id',
        verbose_name=_('item type'),
        help_text=_('Type of resource'),
        blank=False)

    item_file = models.FileField(
        upload_to=get_item_path,
        db_column='item_file',
        verbose_name=_('item file'),
        help_text=_('Upload file associated to file'),
        blank=True,
        null=True)

    media_info = models.JSONField(
        db_column='media_info',
        verbose_name=_('media info'),
        help_text=_('Information of resource file'),
        blank=True,
        null=False)

    source = models.ForeignKey(
        'Source',
        db_column='source_id',
        verbose_name=_('source'),
        help_text=_('Source of item (parsing function and parent directory)'),
        on_delete=models.PROTECT,
        blank=True,
        null=True)

    source_foreign_key = models.CharField(
        db_column='source_foreign_key',
        verbose_name=_('source foreign key'),
        help_text=_('Foreign key of file in source database'),
        max_length=64,
        blank=True)

    metadata = models.JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to item'),
        blank=True,
        null=True)

    captured_on = models.DateTimeField(
        db_column='captured_on',
        verbose_name=_('captured on'),
        help_text=_('Date on which item was produced'),
        blank=True,
        null=True)

    captured_on_year = models.IntegerField(
        db_column='captured_on_year',
        verbose_name=_('year'),
        help_text=_('Year in which the item was captured (YYYY)'),
        blank=True,
        null=True,
        validators=[
            MinValueValidator(1800),
            MaxValueValidator(3000)])

    captured_on_month = models.IntegerField(
        db_column='captured_on_month',
        verbose_name=_('month'),
        help_text=_('Month in which the item was captured (1-12)'),
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(12)])

    captured_on_day = models.IntegerField(
        db_column='captured_on_day',
        verbose_name=_('day'),
        help_text=_('Day in which the item was captured'),
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(32)])

    captured_on_hour = models.IntegerField(
        db_column='captured_on_hour',
        verbose_name=_('hour'),
        help_text=_('Hour of the day in which the item was captured (0 - 23)'),
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(23)])

    captured_on_minute = models.IntegerField(
        db_column='captured_on_minute',
        verbose_name=_('minute'),
        help_text=_('Minute in which the item was captured (0-59)'),
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(59)])

    captured_on_second = models.IntegerField(
        db_column='captured_on_second',
        verbose_name=_('second'),
        help_text=_('Second in which the item was captured (0-59)'),
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(59)])

    captured_on_timezone = models.CharField(
        max_length=256,
        db_column='captured_on_timezone',
        verbose_name=_('timezone'),
        help_text=_('Timezone corresponding to date fields'),
        blank=True,
        null=True)

    licence = models.ForeignKey(
        'Licence',
        db_column='licence_id',
        verbose_name=_('licence'),
        help_text=_('Licence of item'),
        on_delete=models.PROTECT,
        blank=True,
        null=True)

    tags = models.ManyToManyField(
        'Tag',
        verbose_name=_('tags'),
        help_text=_('Tags for item'),
        blank=True)

    ready_event_types = models.ManyToManyField(
        'EventType',
        verbose_name=_('ready event types'),
        help_text=_('Types of event for which item has been fully annotated'),
        blank=True)

    class Meta:
        verbose_name = _('Item')

        verbose_name_plural = _('Items')

        ordering = ['created_on']

        permissions = (
            ("download_item", _("Can download item")),
            ("annotate_item", _("Can annotate item")),
        )

    def __str__(self):
        return str(self.id)

    def clean(self):
        super().clean()

        # Check that reported hash and filesize (if any) coincide with
        # uploaded file.
        self.clean_hash_and_filesize()

        # Check MIME type is valid and registered in the database
        mime_type = self.clean_mime_type()

        # Check that media info is valid for MIME type
        self.clean_media_info(mime_type)

        # Check that mime type is valid for item type
        self.clean_compatible_mime_and_item_types(mime_type)

        # Check that metadata is valid for item type.
        self.clean_metadata()

        # Synchronize captured on individual fields with datetime field.
        self.sync_captured_on()

    def clean_hash_and_filesize(self):
        if self.item_file.name is None and self.hash is None:
            msg = _('If no file is provided, a hash must be given')
            raise ValidationError({'hash': msg})

        if self.item_file.name is None:
            return

        self.item_file.open()
        hash_string = hash_file(self.item_file)
        item_size = self.item_file.size

        if not self.hash:
            self.hash = hash_string
            self.filesize = item_size

        if self.hash != hash_string:
            msg = _('Hash of file and recorded hash do not coincide')
            raise ValidationError({'hash': msg})

    def clean_mime_type(self):
        try:
            return MimeType.infer(file=self.item_file)

        except MimeType.DoesNotExist as error:
            msg = _(
                'No MIME type could be infered or not registered')
            raise ValidationError({'item_file': msg}) from error

    def clean_media_info(self, mime_type):
        try:
            mime_type.validate_media_info(self.media_info)

        except ValidationError as error:
            raise ValidationError({'media_info': error}) from error

    def clean_compatible_mime_and_item_types(self, mime_type):
        try:
            # pylint: disable=no-member
            self.item_type.validate_mime_type(mime_type)

        except ValidationError as error:
            raise ValidationError({'item_file': error}) from error

    def clean_metadata(self):
        try:
            # pylint: disable=no-member
            self.item_type.validate_metadata(self.metadata)

        except ValidationError as error:
            raise ValidationError({'metadata': error}) from error

    def sync_captured_on(self):
        try:
            captured_on = infer_datetime(
                year=self.captured_on_year,
                month=self.captured_on_month,
                day=self.captured_on_day,
                hour=self.captured_on_hour,
                minute=self.captured_on_minute,
                second=self.captured_on_second,
                tz_info=self.captured_on_timezone)
        except ValueError:
            return

        self.captured_on = captured_on

    def delete(self, *args, **kwargs):
        try:
            self.item_file.delete()

        except ValueError:
            pass

        super().delete(*args, **kwargs)