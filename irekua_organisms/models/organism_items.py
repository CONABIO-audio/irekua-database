from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_collections.models import CollectionItem


class OrganismItem(CollectionItem):
    organism = models.ForeignKey(
        "Organism",
        db_column="organism_id",
        verbose_name=_("organism"),
        help_text=_("Organism to which item belongs"),
        on_delete=models.PROTECT,
        blank=False,
        null=False,
    )

    organism_capture = models.ForeignKey(
        "OrganismCapture",
        db_column="organism_capture_id",
        verbose_name=_("organism"),
        help_text=_("Organism to which item belongs"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    organism_observation = models.ForeignKey(
        "OrganismObservation",
        db_column="organism_observation_id",
        verbose_name=_("organism observation"),
        help_text=_("Organism observation to which item belongs"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Organism Item")

        verbose_name_plural = _("Organism Items")

        ordering = ["-created_on"]

    def clean(self):
        # Check that capture and observation are not simultaneously set
        self.clean_organism_item_level()

        if self.organism_capture is not None:
            self.clean_organism_capture_item()

        elif self.organism_observation is not None:
            self.clean_organism_observation_item()

        else:
            self.clean_organism_item()

        # Check that organism and item belong to the same collection
        self.clean_organism_collection()

        super().clean()

    def clean_organism_capture_item(self):
        # Check that the declared organism coincides with the captured organism
        self.clean_captured_organism()

        # Check that this item type can be registered to this capture type
        self.clean_compatible_organism_capture_and_item_type()

    def clean_organism_observation_item(self):
        # Check that the declared organism coincides with the observed organism
        self.clean_captured_organism()

        # Check that this item type can be registered to this observation type
        self.clean_compatible_organism_observation_and_item_type()

    def clean_organism_item(self):
        # Check that item type is valid for organism type
        self.clean_compatible_organism_and_item_type()

    def clean_captured_organism(self):
        if self.organism is None:
            self.organism = self.organism_capture.organism
            return

        if self.organism != self.organism_capture.organism:
            msg = _(
                "The captured organism (%(captured)s) is not the same as "
                "the declared organism (%(declared)s)"
            )
            params = dict(
                captured=self.organism_capture.organism,
                declared=self.organism,
            )
            raise ValidationError({"organism": msg % params})

    def clean_observed_organism(self):
        if self.organism is None:
            self.organism = self.organism_observation.organism
            return

        if self.organism != self.organism_observation.organism:
            msg = _(
                "The observed organism (%(captured)s) is not the same as "
                "the declared organism (%(declared)s)"
            )
            params = dict(
                captured=self.organism_observation.organism,
                declared=self.organism,
            )
            raise ValidationError({"organism": msg % params})

    def clean_organism_item_level(self):
        if self.organism_capture is None or self.organism_observation is None:
            return

        msg = _(
            "You cannot register an item to an organism observation and "
            "organism capture simultaneously"
        )
        raise ValidationError(
            {
                "organism_observation": msg,
                "organism_capture": msg,
            }
        )

    def clean_organism_collection(self):
        if self.collection is None:
            self.collection = self.organism.collection

        # pylint: disable=no-member
        if self.collection != self.organism.collection:
            msg = _(
                "Organism %(organism)s does not belong to the collection "
                "%(collection)s"
            )
            params = dict(organism=self.organism, collection=self.collection)
            raise ValidationError({"organism": msg % params})

    def clean_compatible_organism_and_item_type(self):
        # pylint: disable=no-member
        organism_type = self.organism.organism_type

        try:
            organism_type.validate_item_type(self.item_type)

        except ValidationError as error:
            raise ValidationError({"item_type": error}) from error

    def clean_compatible_organism_observation_and_item_type(self):
        # pylint: disable=no-member
        organism_observation_type = (
            self.organism_observation.organism_observation_type
        )

        try:
            organism_observation_type.validate_item_type(self.item_type)

        except ValidationError as error:
            raise ValidationError({"item_type": error}) from error

    def clean_compatible_organism_capture_and_item_type(self):
        # pylint: disable=no-member
        organism_capture_type = self.organism_capture.organism_capture_type

        try:
            organism_capture_type.validate_item_type(self.item_type)

        except ValidationError as error:
            raise ValidationError({"item_type": error}) from error
