from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_collections.models import SamplingEventItem
from .organism_items import OrganismItemMixin


class OrganismObservationItem(SamplingEventItem, OrganismItemMixin):
    organism_observation = models.ForeignKey(
        "OrganismObservation",
        db_column="organism_observation_id",
        verbose_name=_("organism observation"),
        help_text=_("Organism observation to which item belongs"),
        on_delete=models.PROTECT,
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = _("Organism Observation Item")

        verbose_name_plural = _("Organism Observation Items")

        ordering = ["-created_on"]

    def clean(self):
        # Check the captured organims coincides with the organism field
        self.clean_same_organism()

        super().clean()

    def clean_same_organism(self):
        # pylint: disable=no-member
        observed_organism = self.organism_observation.organism

        if self.organism is None:
            self.organism = observed_organism
            return

        if observed_organism != self.organism:
            msg = _(
                "The declared observed organism %(observed_organism)s does "
                "not coincide with the declared organism %(organism)s"
            )
            params = dict(observed_organism=observed_organism, organism=self.organism)
            raise ValidationError({"observed_organism": msg % params})

    def clean_compatible_item_type(self):
        # pylint: disable=no-member
        organism_observation_type = self.organism_observation.organism_observation_type

        try:
            organism_observation_type.validate_item_type(self.item_type)

        except ValidationError as error:
            raise ValidationError({"item_type": error}) from error
