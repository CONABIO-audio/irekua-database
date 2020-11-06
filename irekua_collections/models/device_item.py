"""Device Item Module."""
import os

from django.db import models
from django.utils.translation import gettext_lazy as _

from .collection_items import CollectionItem


class DeviceItem(CollectionItem):
    """Device Item Model."""

    upload_to_format = os.path.join(
            'items',
            '{collection}',
            '{sampling_event}',
            '{hash}{ext}'
            )

    collection_device = models.ForeignKey(
            'CollectionDevice',
            models.PROTECT,
            db_column='collection_device_id',
            verbose_name=_('collection device'),
            help_text=_('Device that generated this item'),
            blank=False,
            null=False)

    class Meta:
        verbose_name = _('Device Item')

        verbose_name_plural = _('Device Items')

        ordering = ['-created_on']
