from django.db import models

from django.utils.translation import gettext_lazy as _
from irekua_database.base import IrekuaModelBase
from irekua_types.models import LicenceType
from irekua_collections.mixins import CollectionMetadataSchemaMixin


class CollectionTypeLicenceType(IrekuaModelBase, CollectionMetadataSchemaMixin):
    collection_type = models.ForeignKey(
        'CollectionType',
        on_delete=models.CASCADE,
        db_column='collection_type_id',
        verbose_name=_('collection type'),
        help_text=_('Collection type in which this licence type is permitted'),
        blank=False,
        null=False)

    licence_type = models.ForeignKey(
        LicenceType,
        on_delete=models.PROTECT,
        db_column='licence_type_id',
        verbose_name=_('licence type'),
        help_text=_('Licence type to be admissible in collections of this type'),
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Collection Type Licence Type')
        verbose_name_plural = _('Collection Type Licence Types')

        unique_together = (
            ('collection_type', 'licence_type'),
        )

    def __str__(self):
        msg = _('Collection %(collection)s: Licence Type %(licence)s')
        params = dict(
            licence=str(self.licence_type),
            collection=str(self.collection_type))
        return msg % params
