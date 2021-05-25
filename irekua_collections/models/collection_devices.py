from django.db import models
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBaseUser
from irekua_devices.models import PhysicalDevice


class CollectionDevice(IrekuaModelBaseUser):
    physical_device = models.ForeignKey(
        PhysicalDevice,
        on_delete=models.PROTECT,
        db_column="physical_device_id",
        verbose_name=_("physical device"),
        help_text=_("Reference to physical device"),
        blank=False,
        null=False,
    )

    collection = models.ForeignKey(
        "Collection",
        on_delete=models.CASCADE,
        db_column="collection_id",
        verbose_name=_("collection"),
        help_text=_("Collection to which the device belongs"),
        blank=False,
        null=False,
    )

    collection_name = models.CharField(
        max_length=64,
        db_column="collection_name",
        verbose_name=_("Name within collection"),
        help_text=_(
            "Nmae of device within the collection "
            "(visible to all collection users)"
        ),
        blank=True,
    )

    collection_metadata = models.JSONField(
        blank=True,
        db_column="collection_metadata",
        verbose_name=_("collection metadata"),
        help_text=_("Metadata associated with device within collection"),
        null=True,
    )

    class Meta:
        verbose_name = _("Collection Device")

        verbose_name_plural = _("Collection Devices")

        ordering = ["-modified_on"]

        unique_together = (
            ("physical_device", "collection"),
            ("collection", "collection_name"),
        )

    def __str__(self):
        if self.collection_name:
            return self.collection_name

        return _("Collection device {}").format(self.id)

    def clean(self):
        super().clean()

        # pylint: disable=no-member
        collection_type = self.collection.collection_type

        # If collection type does not restrict device type no more
        # validation is necessary
        if not collection_type.restrict_device_types:
            return

        # Get device type configuration from collection type
        device_type_config = self.clean_allowed_device_type(collection_type)

        # Check additional metadata is valid for device type
        self.clean_valid_collection_metadata(device_type_config)

    def clean_allowed_device_type(self, collection_type):
        # pylint: disable=no-member
        device_type = self.physical_device.device.device_type

        try:
            return collection_type.get_device_type(device_type)

        except ObjectDoesNotExist as error:
            msg = _(
                "Devices of type %(device_type)s are not allowed in "
                "collections of type %(collection_type)s"
            )
            params = dict(
                device_type=device_type,
                collection_type=collection_type,
            )
            raise ValidationError({"physical_device": msg % params}) from error

    def clean_valid_collection_metadata(self, device_type_config):
        try:
            device_type_config.validate_metadata(self.collection_metadata)

        except ValidationError as error:
            raise ValidationError(
                {"collection_metadata": str(error)}
            ) from error

    @property
    def items(self):
        from irekua_collections.models import CollectionItem

        return CollectionItem.objects.filter(collection_device=self)
