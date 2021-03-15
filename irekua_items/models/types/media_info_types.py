from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase
from irekua_schemas.models import Schema


class MediaInfoType(IrekuaModelBase):
    name = models.CharField(
        max_length=64,
        db_column="name",
        verbose_name=_("name"),
        unique=True,
        help_text=_("Name of media info type"),
        blank=False,
    )

    description = models.TextField(
        db_column="description",
        verbose_name=_("description"),
        help_text=_("Description of media info type"),
        blank=False,
    )

    media_info_schema = models.ForeignKey(
        Schema,
        models.PROTECT,
        db_column="media_info_schema_id",
        verbose_name=_("media info schema"),
        help_text=_("JSON Schema for media info"),
        null=False,
        blank=False,
    )

    class Meta:
        verbose_name = _("Media Info Type")

        verbose_name_plural = _("Media Info Types")

        ordering = ["-created_on"]

    def __str__(self):
        return self.name

    def validate_media_info(self, media_info):
        if self.media_info_schema is None:
            return

        try:
            # pylint: disable=no-member
            self.media_info_schema.validate(media_info)

        except ValidationError as error:
            msg = _("Media info is not valid. Error: %(error)s")
            params = dict(error=error)
            raise ValidationError(msg % params) from error
