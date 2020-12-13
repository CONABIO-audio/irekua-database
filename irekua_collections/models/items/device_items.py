import os

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_items.models import Item
from .collection_items import CollectionItemMixin


class DeviceItemMixin(CollectionItemMixin):
    collection_device = models.ForeignKey(
        "CollectionDevice",
        db_column="collection_device_id",
        verbose_name=_("collection device"),
        help_text=_("Device used to capture the item"),
        on_delete=models.PROTECT,
        blank=False,
        null=False,
    )

    class Meta:
        abstract = True

    def clean(self):
        super().clean()
        # Check that collection device belongs and
        # collection coincide
        self.clean_compatible_device_and_collection()

    def clean_compatible_device_and_collection(self):
        if self.collection is None:
            # pylint: disable=no-member
            self.collection = self.collection_device.collection

        # pylint: disable=no-member
        if self.collection == self.collection_device.collection:
            return

        msg = _(
            "The device used to capture the item (%(collection_device)s) does "
            "not belong to the collection %(collection)s."
        )
        params = dict(
            collection_device=self.collection_device,
            collection=self.collection,
        )
        raise ValidationError({"collection_device": msg % params})


class DeviceItem(Item, DeviceItemMixin):
    upload_to_format = os.path.join(
        "items",
        "collection" "{collection}",
        "device" "{device}",
        "{hash}{ext}",
    )

    class Meta:
        verbose_name = _("Device Item")

        verbose_name_plural = _("Device Items")

        ordering = ["-created_on"]

    def clean_allowed_item_level(self, item_type_config):
        if not item_type_config.device_item:
            msg = _(
                "Item of type %(item_type)s are cannot be declared at the device "
                "level for collections of type %(collection_type)s"
            )
            params = dict(
                item_type=self.item_type,
                collection_type=item_type_config.collection_type,
            )
            raise ValidationError({"item_type": msg % params})

    def get_upload_to_format_arguments(self):
        return {
            **super().get_upload_to_format_arguments(),
            # pylint: disable=no-member
            "device": self.collection_device.id,
        }
