from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase
from irekua_collections.models import CollectionType


class CollectionTypeOrganismConfig(IrekuaModelBase):
    collection_type = models.OneToOneField(
        CollectionType,
        on_delete=models.CASCADE,
        help_text=_("Collection Type to be configured."),
        primary_key=True,
    )

    use_organisms = models.BooleanField(
        db_column="use_organisms",
        verbose_name=_("use organisms"),
        help_text=_(
            "Boolean flag indicating whether organisms are to be used "
            "in this collection type."
        ),
        blank=False,
        null=False,
        default=False,
    )

    restrict_organism_types = models.BooleanField(
        db_column="restrict_organism_types",
        verbose_name=_("restrict organism types"),
        help_text=_(
            "Flag indicating whether types of organisms are restricted to "
            "registered ones"
        ),
        default=True,
        null=False,
        blank=True,
    )

    restrict_organism_observation_types = models.BooleanField(
        db_column="restrict_organism_observation_types",
        verbose_name=_("restrict organism observation types"),
        help_text=_(
            "Flag indicating whether types of organism observation are restricted to "
            "registered ones"
        ),
        default=True,
        null=False,
        blank=True,
    )

    restrict_organism_capture_types = models.BooleanField(
        db_column="restrict_organism_capture_types",
        verbose_name=_("restrict organism capture types"),
        help_text=_(
            "Flag indicating whether types of organism captures are restricted to "
            "registered ones"
        ),
        default=True,
        null=False,
        blank=True,
    )

    organism_types = models.ManyToManyField(
        "OrganismType",
        through="CollectionTypeOrganismType",
        through_fields=("collection_type_organism_config", "organism_type"),
        verbose_name=_("organism types"),
        help_text=_(
            "Types of organisms that can be registered into "
            "collections of this type."
        ),
        blank=True,
    )

    organism_observation_types = models.ManyToManyField(
        "OrganismObservationType",
        through="CollectionTypeOrganismObservationType",
        through_fields=(
            "collection_type_organism_config",
            "organism_observation_type",
        ),
        verbose_name=_("organism observation types"),
        help_text=_(
            "Types of organism observation that can be registered into "
            "collections of this type."
        ),
        blank=True,
    )

    organism_capture_types = models.ManyToManyField(
        "OrganismCaptureType",
        through="CollectionTypeOrganismCaptureType",
        through_fields=(
            "collection_type_organism_config",
            "organism_capture_type",
        ),
        verbose_name=_("organism capture types"),
        help_text=_(
            "Types of organism captures that can be registered into "
            "collections of this type."
        ),
        blank=True,
    )

    class Meta:
        verbose_name = _("Collection Type Organism Configuration")

        verbose_name_plural = _("Collection Type Organism Configurations")

        ordering = ["-created_on"]

    def __str__(self):
        msg = _("%(col_type)s - Organism Configuration")
        params = dict(col_type=self.collection_type.name)
        return msg % params

    def get_organism_type(self, organism_type):
        return self.organism_types.through.objects.get(
            collection_type_organism_config=self,
            organism_type=organism_type,
        )

    def get_organism_capture_type(self, organism_capture_type):
        return self.organism_capture_types.through.objects.get(
            collection_type_organism_config=self,
            organism_capture_type=organism_capture_type,
        )
