from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_items.models import Item


class CollectionItem(Item):
    collection = models.ForeignKey(
        'Collection',
        db_column='collection_id',
        verbose_name=_('collection'),
        help_text=_('Collection to which this item belongs'),
        on_delete=models.PROTECT,
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Collection Item')
        verbose_name_plural = _('Collection Items')
