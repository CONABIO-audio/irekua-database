from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from irekua_database.base import IrekuaModelBase
from irekua_schemas.mixins import MetadataSchemaMixin
from irekua_schemas.models import Schema


class Device(IrekuaModelBase, MetadataSchemaMixin):
    device_type = models.ForeignKey(
        "DeviceType",
        on_delete=models.PROTECT,
        related_name="device_type",
        db_column="device_type_id",
        verbose_name=_("device type"),
        help_text=_("Type of device"),
        blank=False,
    )

    brand = models.ForeignKey(
        "DeviceBrand",
        on_delete=models.PROTECT,
        related_name="device_brand",
        db_column="device_brand_id",
        verbose_name=_("brand"),
        help_text=_("Brand of device"),
        blank=False,
    )

    model = models.CharField(
        max_length=64,
        db_column="model",
        verbose_name=_("model"),
        help_text=_("Model of device"),
        blank=False,
    )

    configuration_schema = models.ForeignKey(
        Schema,
        models.PROTECT,
        related_name="configuration_schema",
        db_column="configuration_schema_id",
        verbose_name=_("configuration schema"),
        help_text=_("JSON Schema for configuration info of device"),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Device")

        verbose_name_plural = _("Devices")

        unique_together = ("brand", "model")

        ordering = ["brand", "model"]

    def __str__(self):
        msg = "%(device_type)s: %(brand)s - %(model)s"
        params = dict(device_type=self.device_type, brand=self.brand, model=self.model)
        return msg % params

    def validate_configuration(self, configuration):
        if self.configuration_schema is None:
            return

        try:
            self.configuration_schema.validate(configuration)
        except ValidationError as error:
            msg = _("Invalid device configuration. Error: %(error)s")
            params = dict(error=str(error))
            raise ValidationError(msg, params=params) from error
