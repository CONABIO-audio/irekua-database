from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase
from irekua_collections.mixins import CollectionMetadataSchemaMixin

class CollectionTypeOrganismCaptureType(IrekuaModelBase, CollectionMetadataSchemaMixin):
    collection_type_organism_config = models.ForeignKey(
        'CollectionTypeOrganismConfig',
        on_delete=models.CASCADE,
        db_column='collection_type_organism_config_id',
        verbose_name=_('collection type organism config'),
        help_text=_('Collection type organism configuration'),
        blank=False,
        null=False)

    organism_capture_type = models.ForeignKey(
        'OrganismCaptureType',
        on_delete=models.PROTECT,
        db_column='organism_capture_type_id',
        verbose_name=_('organism capture type'),
        help_text=_('Organism capture type to be registered to the collection type'),
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Collection Type Organism Capture Type')

        verbose_name_plural = _('Collection Type Organism Capture Types')

        ordering = ['-created_on']

        unique_together = (
            ('collection_type_organism_config', 'organism_capture_type'),
        )
