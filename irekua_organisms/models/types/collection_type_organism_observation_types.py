from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase
from irekua_collections.mixins import CollectionMetadataSchemaMixin


class CollectionTypeOrganismObservationType(
    IrekuaModelBase,
    CollectionMetadataSchemaMixin,
):
    collection_type_organism_config = models.ForeignKey(
        "CollectionTypeOrganismConfig",
        on_delete=models.CASCADE,
        db_column="collection_type_organism_config_id",
        verbose_name=_("collection type organism config"),
        help_text=_("Collection type organism configuration"),
        blank=False,
        null=False,
    )

    organism_observation_type = models.ForeignKey(
        "OrganismObservationType",
        on_delete=models.PROTECT,
        db_column="organism_observation_type_id",
        verbose_name=_("organism observation type"),
        help_text=_(
            "Organism observation type to be registered to the collection type"
        ),
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = _("Collection Type Organism Observation Type")

        verbose_name_plural = _("Collection Type Organism Observation Types")

        ordering = ["-created_on"]

        unique_together = (
            ("collection_type_organism_config", "organism_observation_type"),
        )
