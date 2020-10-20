from django.db import models

from django.utils.translation import gettext_lazy as _
from irekua_database.base import IrekuaModelBase
from irekua_types.models import DeploymentType
from irekua_collections.mixins import CollectionMetadataSchemaMixin


class CollectionTypeDeploymentType(IrekuaModelBase, CollectionMetadataSchemaMixin):
    collection_type = models.ForeignKey(
        'CollectionType',
        on_delete=models.CASCADE,
        db_column='collection_type_id',
        verbose_name=_('collection type'),
        help_text=_('Collection type in which this deployment type is permitted'),
        blank=False,
        null=False)

    deployment_type = models.ForeignKey(
        DeploymentType,
        on_delete=models.PROTECT,
        db_column='deployment_type_id',
        verbose_name=_('deployment type'),
        help_text=_('Deployment type to be admissible in collections of this type'),
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Collection Type Deployment Type')
        verbose_name_plural = _('Collection Type Deployment Types')

        unique_together = (
            ('collection_type', 'deployment_type'),
        )

    def __str__(self):
        msg = _('Collection %(collection)s: Deployment Type %(deployment)s')
        params = dict(
            deployment=str(self.deployment_type),
            collection=str(self.collection_type))
        return msg % params
