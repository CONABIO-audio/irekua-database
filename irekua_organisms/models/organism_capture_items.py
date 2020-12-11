from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_collections.models import DeploymentItem
from .organism_items import OrganismItemMixin


class OrganismCaptureItem(DeploymentItem, OrganismItemMixin):
    capture = models.ForeignKey(
        "OrganismCapture",
        db_column="organism_capture_id",
        verbose_name=_("organism"),
        help_text=_("Organism to which item belongs"),
        on_delete=models.PROTECT,
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = _("Organism Capture Item")

        verbose_name_plural = _("Organism Capture Items")

        ordering = ["-created_on"]

    def clean(self):
        super().clean()

        # Check the captured organims coincides with the organism field
        self.clean_same_organism()

    def clean_same_organism(self):
        # pylint: disable=no-member
        captured_organism = self.capture.organism

        if captured_organism != self.organism:
            msg = _(
                "The declared captured organism %(captured_organism)s does "
                "not coincide with the declared organism %(organism)s"
            )
            params = dict(captured_organism=captured_organism, organism=self.organism)
            raise ValidationError({"captured_organism": msg % params})

    def clean_compatible_item_type(self):
        # pylint: disable=no-member
        organism_capture_type = self.capture.organism_capture_type

        try:
            organism_capture_type.validate_item_type(self.item_type)

        except ValidationError as error:
            raise ValidationError({"item_type": error}) from error
