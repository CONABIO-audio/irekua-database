import mimetypes
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase
from irekua_schemas.models import Schema


mimetypes.init()


class MimeType(IrekuaModelBase):
    MIME_TYPES = [
        (value, value) for value in
        sorted(list(set(mimetypes.types_map.values())))
    ]

    mime_type = models.CharField(
        max_length=128,
        unique=True,
        choices=MIME_TYPES,
        db_column='media_type',
        verbose_name=_('media type'),
        help_text=_('MIME types associated with item type'),
        blank=False)

    media_info_schema = models.ForeignKey(
        Schema,
        models.PROTECT,
        related_name='media_info_schema',
        db_column='media_info_schema_id',
        verbose_name=_('media info schema'),
        help_text=_('JSON Schema for item type media info'),
        null=True,
        blank=True)

    class Meta:
        verbose_name = _('Mime Type')
        verbose_name_plural = _('Mime Types')

        ordering = ['mime_type']

    def __str__(self):
        return self.mime_type

    def validate_media_info(self, media_info):
        try:
            self.media_info_schema.validate(media_info)
        except ValidationError as error:
            msg = _(
                'Invalid media info for item of type %(type)s. '
                'Error %(error)s')
            params = dict(type=str(self), error=str(error))
            raise ValidationError(msg, params=params) from error

    @staticmethod
    def infer(name=None, url=None, file=None):
        if url is not None:
            name = url

        if file is not None:
            name = file.name

        if name is None:
            msg = _('A name, url or file must be provided')
            raise ValueError(msg)

        mime_type_name = mimetypes.guess_type(name)[0]
        return MimeType.objects.get(mime_type=mime_type_name)