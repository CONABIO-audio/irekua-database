from django.db import models

from django.utils.translation import gettext_lazy as _
from irekua_database.base import IrekuaModelBase
from irekua_collections.mixins import CollectionMetadataSchemaMixin
# from irekua_types.models import SamplingEventType


class CollectionTypeSamplingEventType(IrekuaModelBase, CollectionMetadataSchemaMixin):
    collection_type = models.ForeignKey(
        'CollectionType',
        on_delete=models.CASCADE,
        db_column='collection_type_id',
        verbose_name=_('collection type'),
        help_text=_('Collection type in which this sampling event type is permitted'),
        blank=False,
        null=False)

    sampling_event_type = models.ForeignKey(
        'SamplingEventType',
        on_delete=models.PROTECT,
        db_column='sampling_event_type_id',
        verbose_name=_('sampling event type'),
        help_text=_('Sampling Event type to be admissible in collections of this type'),
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Collection Type Sampling Event Type')
        verbose_name_plural = _('Collection Type Sampling Event Types')

        unique_together = (
            ('collection_type', 'sampling_event_type'),
        )

    def __str__(self):
        msg = _('Collection %(collection)s: Sampling Event Type %(sampling_event)s')
        params = dict(
            sampling_event=str(self.sampling_event_type),
            collection=str(self.collection_type))
        return msg % params
