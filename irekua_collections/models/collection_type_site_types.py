from django.db import models

from django.utils.translation import gettext_lazy as _
from irekua_database.base import IrekuaModelBase
from irekua_types.models import SiteType
from irekua_collections.mixins import CollectionMetadataSchemaMixin


class CollectionTypeSiteType(IrekuaModelBase, CollectionMetadataSchemaMixin):
    collection_type = models.ForeignKey(
        'CollectionType',
        on_delete=models.CASCADE,
        db_column='collection_type_id',
        verbose_name=_('collection type'),
        help_text=_('Collection type in which this site type is permitted'),
        blank=False,
        null=False)

    site_type = models.ForeignKey(
        SiteType,
        on_delete=models.PROTECT,
        db_column='site_type_id',
        verbose_name=_('site type'),
        help_text=_('Site type to be admissible in collections of this type'),
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Collection Type Site Type')
        verbose_name_plural = _('Collection Type Site Types')

        unique_together = (
            ('collection_type', 'site_type'),
        )

    def __str__(self):
        msg = _('Collection %(collection)s: Site Type %(site)s')
        params = dict(
            site=str(self.site_type),
            collection=str(self.collection_type))
        return msg % params
