from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase
from irekua_schemas.mixins import MetadataSchemaMixin
from irekua_items.models import MimeType


class DeviceType(IrekuaModelBase, MetadataSchemaMixin):
    name = models.CharField(
        max_length=64,
        unique=True,
        db_column="name",
        verbose_name=_("name"),
        help_text=_("Name for device type"),
        blank=False,
    )

    description = models.TextField(
        db_column="description",
        verbose_name=_("description"),
        help_text=_("Description of device type"),
        blank=False,
    )

    icon = models.ImageField(
        db_column="icon",
        verbose_name=_("icon"),
        help_text=_("Icon for device type"),
        upload_to="images/device_types/",
        blank=True,
        null=True,
    )

    mime_types = models.ManyToManyField(
        MimeType,
        db_column="mime_types",
        verbose_name=_("mime types"),
        help_text=_("Possible mime types for files generated by devices of this type"),
        blank=True,
    )

    class Meta:
        verbose_name = _("Device Type")
        verbose_name_plural = _("Device Types")

        ordering = ["name"]

    def validate_mime_type(self, mime_type):
        if not self.mime_types.filter(pk=mime_type.pk).exists():
            msg = _(
                "Device type %(device_type)s do not "
                "support files of mime type %(mime_type)s"
            )
            params = dict(device_type=self.name, mime_type=mime_type)
            raise ValidationError(msg % params)

    def __str__(self):
        return self.name
