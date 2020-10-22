from django.db import models

from django.utils.translation import gettext_lazy as _
from irekua_database.base import IrekuaModelBase
from irekua_items.models import ItemType
from irekua_collections.mixins import CollectionMetadataSchemaMixin


class CollectionTypeItemType(IrekuaModelBase, CollectionMetadataSchemaMixin):
    collection_type = models.ForeignKey(
        'CollectionType',
        on_delete=models.CASCADE,
        db_column='collection_type_id',
        verbose_name=_('collection type'),
        help_text=_('Collection type in which this item type is permitted'),
        blank=False,
        null=False)

    item_type = models.ForeignKey(
        ItemType,
        on_delete=models.PROTECT,
        db_column='item_type_id',
        verbose_name=_('item type'),
        help_text=_('Item to be part of collection'),
        blank=False,
        null=False)

    collection_item = models.BooleanField(
        db_column='collection_item',
        verbose_name=_('collection item'),
        help_text=_(
            'Boolean flag indicating items of this type can be registered '
            'at the collection level.'),
        blank=True,
        default=True,
        null=False)

    sampling_event_item = models.BooleanField(
        db_column='sampling_event_item',
        verbose_name=_('sampling event item'),
        help_text=_(
            'Boolean flag indicating items of this type can be registered '
            'at the sampling event level.'),
        blank=True,
        default=True,
        null=False)

    deployment_item = models.BooleanField(
        db_column='deployment_item',
        verbose_name=_('deployment item'),
        help_text=_(
            'Boolean flag indicating items of this type can be registered '
            'at the deployment level.'),
        blank=True,
        default=True,
        null=False)

    class Meta:
        verbose_name = _('Collection Type Item Type')
        verbose_name_plural = _('Collection Type Item Types')

        unique_together = (
            ('collection_type', 'item_type'),
        )

    def __str__(self):
        msg = _('Collection %(collection)s: Item Type %(item)s')
        params = dict(
            item=str(self.item_type),
            collection=str(self.collection_type))
        return msg % params
