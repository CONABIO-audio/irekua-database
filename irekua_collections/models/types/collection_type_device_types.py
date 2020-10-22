from django.db import models

from django.utils.translation import gettext_lazy as _
from irekua_database.base import IrekuaModelBase

from irekua_devices.models import DeviceType
from irekua_collections.mixins import CollectionMetadataSchemaMixin


class CollectionTypeDeviceType(IrekuaModelBase, CollectionMetadataSchemaMixin):
    collection_type = models.ForeignKey(
        'CollectionType',
        on_delete=models.CASCADE,
        db_column='collection_type_id',
        verbose_name=_('collection type'),
        help_text=_('Collection type in which device type is permitted'),
        blank=False,
        null=False)

    device_type = models.ForeignKey(
        DeviceType,
        on_delete=models.PROTECT,
        db_column='device_type_id',
        verbose_name=_('device type'),
        help_text=_('Device to be part of collection'),
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Collection Type Device Type')
        verbose_name_plural = _('Collection Type Device Types')

        unique_together = (
            ('collection_type', 'device_type'),
        )

    def __str__(self):
        msg = _('Collection %(collection_type)s: Device Type %(device_type)s')
        params = dict(
            device_type=str(self.device_type),
            collection_type=str(self.collection_type))
        return msg % params
