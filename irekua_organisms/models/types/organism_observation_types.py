from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from irekua_database.base import IrekuaModelBase
from irekua_schemas.mixins import MetadataSchemaMixin
from irekua_terms.models import TermType
from irekua_items.models import ItemType
from irekua_collections.models import SamplingEventType


class OrganismObservationType(IrekuaModelBase, MetadataSchemaMixin):
    name = models.CharField(
        max_length=64,
        db_column="name",
        verbose_name=_("name"),
        unique=True,
        help_text=_("Name of organism observation type"),
        blank=False,
    )

    description = models.TextField(
        db_column="description",
        verbose_name=_("description"),
        help_text=_("Description of organism capture type"),
        blank=False,
    )

    icon = models.ImageField(
        db_column="icon",
        verbose_name=_("icon"),
        help_text=_("Organism observation type icon"),
        upload_to="images/organism_observation_types/",
        blank=True,
        null=True,
    )

    organism_type = models.ForeignKey(
        "OrganismType",
        on_delete=models.CASCADE,
        db_column="organism_type_id",
        verbose_name=_("organism type"),
        help_text=_("Organism type being observed"),
        blank=False,
        null=False,
    )

    sampling_event_types = models.ManyToManyField(
        SamplingEventType,
        verbose_name=_("sampling event types"),
        help_text=_(
            "Sampling event types on which this types of observation are made"
        ),
        blank=False,
    )

    term_types = models.ManyToManyField(
        TermType,
        verbose_name=_("term types"),
        help_text=_("Valid term types to describe the organism observation"),
        blank=True,
    )

    restrict_item_types = models.BooleanField(
        db_column="restrict_item_types",
        verbose_name=_("restrict item types"),
        help_text=_(
            "Flag indicating whether any type of item can be associated "
            "to observations of this type"
        ),
        default=True,
        null=False,
        blank=True,
    )

    item_types = models.ManyToManyField(
        ItemType,
        verbose_name=_("item types"),
        help_text=_(
            "Types of items that can be associated to "
            "organism observations of this type."
        ),
        blank=True,
    )

    class Meta:
        verbose_name = _("Organism Observation Type")

        verbose_name_plural = _("Organism Observation Types")

        ordering = ["-created_on"]

    def __str__(self):
        return str(self.name)

    def validate_sampling_event_type(self, sampling_event_type):
        if not self.sampling_event_types.filter(
            pk=sampling_event_type.pk
        ).exists():
            msg = _(
                "Organisms observations of type %(observation_type)s cannot be "
                "registered in sampling events of type %(sampling_event_type)s"
            )
            params = dict(
                sampling_event_type=sampling_event_type,
                observation_type=self,
            )
            raise ValidationError(msg % params)

    def validate_item_type(self, item_type):
        if not self.item_types.filter(id=item_type.id).exists():
            msg = _(
                "Items of type %(item_type)s can not be associated to organism "
                "observations of type %(observation_type)s."
            )
            params = dict(item_type=item_type, observation_type=self)
            raise ValidationError(msg % params)

    def validate_term(self, term):
        if not self.term_types.filter(id=term.term_type.id).exists():
            msg = _(
                "Terms of type %(term_type)s are not allowed for organism observations "
                " of type %(observation_type)s. Term: %(term)s"
            )
            params = dict(
                term_type=term.term_type.name,
                observation_type=self,
                term=term.value,
            )
            raise ValidationError(msg % params)
