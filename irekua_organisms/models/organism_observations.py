from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from irekua_database.base import IrekuaModelBaseUser
from irekua_collections.models import SamplingEvent
from irekua_terms.models import Term


class OrganismObservation(IrekuaModelBaseUser):
    organism_observation_type = models.ForeignKey(
        "OrganismObservationType",
        db_column="organism_observation_type_id",
        verbose_name=_("organism observation type"),
        help_text=_("Observation type"),
        on_delete=models.PROTECT,
        blank=False,
        null=False,
    )

    sampling_event = models.ForeignKey(
        SamplingEvent,
        db_column="sampling_event_id",
        verbose_name=_("sampling_event"),
        help_text=_("Sampling event in which the organism was observed"),
        on_delete=models.PROTECT,
        blank=False,
        null=False,
    )

    organism = models.ForeignKey(
        "Organism",
        db_column="organism_id",
        verbose_name=_("organism"),
        help_text=_("Observed organism"),
        on_delete=models.PROTECT,
        blank=False,
        null=False,
    )

    metadata = models.JSONField(
        db_column="metadata",
        verbose_name=_("metadata"),
        help_text=_("Additional metadata associated to organism observation"),
        blank=True,
        null=True,
    )

    collection_metadata = models.JSONField(
        db_column="collection_metadata",
        verbose_name=_("collection metadata"),
        help_text=_(
            "Additional metadata associated to organism observation in collection"
        ),
        blank=True,
        null=True,
    )

    labels = models.ManyToManyField(
        Term,
        verbose_name=_("labels"),
        help_text=_("Description of the organism observation"),
        blank=True,
    )

    class Meta:
        verbose_name = _("Organism Observation")

        verbose_name_plural = _("Organism Observations")

        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.organism_observation_type.name} {self.id}"

    def clean(self):
        super().clean()

        #  Check if collection has been configured to use organisms
        organism_config = self.clean_organism_config()

        # Check if collection type allows organisms
        self.clean_collection_type(organism_config)

        # Check that observation type is valid for organism type
        self.clean_compatible_organism_and_observation_type()

        # Check that additional metadata is valid for observation type
        self.clean_metadata()

        # No futher validation is required if organism observation types are not
        # restricted
        if not organism_config.restrict_organism_observation_types:
            return

        # Check organism capture type is allowed in collections of this type
        organism_observation_type_config = (
            self.clean_organism_observation_type(organism_config)
        )

        # Check that additional collection metadata is valid for organism observation type
        self.clean_collection_metadata(organism_observation_type_config)

    def clean_organism_config(self):
        # pylint: disable=no-member
        collection_type = self.collection.collection_type

        try:
            return collection_type.collectiontypeorganismconfig

        except ObjectDoesNotExist as error:
            msg = _(
                "Collections of type %(collection_type)s do not allow organisms."
            )
            params = dict(collection_type=collection_type)
            raise ValidationError({"collection": msg % params}) from error

    # pylint: disable=no-self-use
    def clean_collection_type(self, organism_config):
        if not organism_config.use_organisms:
            raise ValidationError(
                _("This collection does not allow organisms")
            )

    def clean_compatible_organism_and_observation_type(self):
        # pylint: disable=no-member
        if (
            self.organism.organism_type
            != self.organism_observation_type.organism_type
        ):
            msg = _(
                "Observations of type %(capture_type)s cannot be registered on organisms "
                "of type %(organism_type)s"
            )
            # pylint: disable=no-member
            params = dict(
                capture_type=self.organism_observation_type,
                organism_type=self.organism.organism_type,
            )
            raise ValidationError({"organism_observation_type": msg % params})

    def clean_metadata(self):
        try:
            # pylint: disable=no-member
            self.organism_observation_type.validate_metadata(self.metadata)

        except ValidationError as error:
            raise ValidationError({"metadata": error}) from error

    def clean_organism_observation_type(self, organism_config):
        try:
            return organism_config.get_organism_observation_type(
                self.organism_observation_type
            )

        except ObjectDoesNotExist as error:
            raise ValidationError(
                {"organism_observation_type": error}
            ) from error

    def clean_collection_metadata(self, organism_observation_type_config):
        try:
            organism_observation_type_config.validate_metadata(
                self.collection_metadata
            )

        except ValidationError as error:
            raise ValidationError({"collection_metadata": error}) from error

    def collection(self):
        return self.organism.collection
