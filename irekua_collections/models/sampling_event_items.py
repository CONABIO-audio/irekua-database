from django.db import models
from django.utils.translation import gettext_lazy as _

from .collection_items import CollectionItem


class SamplingEventItem(CollectionItem):
    sampling_event = models.ForeignKey(
        'SamplingEvent',
        db_column='sampling_event_id',
        verbose_name=_('sampling event'),
        help_text=_('Sampling event in which this item was captured'),
        on_delete=models.PROTECT,
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Sampling Event Item')
        verbose_name_plural = _('Sampling Event Items')
