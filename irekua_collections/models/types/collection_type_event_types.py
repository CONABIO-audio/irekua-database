from django.db import models

from django.utils.translation import gettext_lazy as _
from irekua_database.base import IrekuaModelBase
from irekua_annotations.models import EventType
from irekua_collections.mixins import CollectionMetadataSchemaMixin


class CollectionTypeEventType(IrekuaModelBase, CollectionMetadataSchemaMixin):
    collection_type = models.ForeignKey(
        'CollectionType',
        on_delete=models.CASCADE,
        db_column='collection_type_id',
        verbose_name=_('collection type'),
        help_text=_('Collection type in which this event type is permitted'),
        blank=False,
        null=False)

    event_type = models.ForeignKey(
        EventType,
        on_delete=models.PROTECT,
        db_column='event_type_id',
        verbose_name=_('event type'),
        help_text=_('Event type to be admissible in collections of this type'),
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Collection Type Event Type')
        verbose_name_plural = _('Collection Type Event Types')

        unique_together = (
            ('collection_type', 'event_type'),
        )

    def __str__(self):
        msg = _('Collection %(collection)s: Event Type %(event)s')
        params = dict(
            event=str(self.event_type),
            collection=str(self.collection_type))
        return msg % params
