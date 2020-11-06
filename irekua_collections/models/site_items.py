"""Site Item Module."""
import os

from django.db import models
from django.utils.translation import gettext_lazy as _

from .collection_items import CollectionItem


class SiteItem(CollectionItem):
    """Site Item Model."""

    upload_to_format = os.path.join(
            'items',
            '{collection}',
            '{sampling_event}',
            '{hash}{ext}'
            )

    collection_site = models.ForeignKey(
            'CollectionSite',
            models.PROTECT,
            db_column='collection_site_id',
            verbose_name=_('collection site'),
            help_text=_('Site in which this item was captured'),
            blank=False,
            null=False)

    class Meta:
        verbose_name = _('Site Item')

        verbose_name_plural = _('Site Items')

        ordering = ['-created_on']
