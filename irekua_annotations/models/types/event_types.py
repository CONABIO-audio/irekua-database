from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase
from irekua_schemas.mixins import MetadataSchemaMixin
from irekua_terms.models import TermType
from irekua_terms.models import Term
from irekua_items.models import ItemType


class EventType(IrekuaModelBase, MetadataSchemaMixin):
    name = models.CharField(
        max_length=64,
        unique=True,
        db_column="name",
        verbose_name=_("name"),
        help_text=_("Name of event type"),
        blank=False,
    )

    description = models.TextField(
        db_column="description",
        verbose_name=_("description"),
        help_text=_("Description of event type"),
        blank=False,
    )

    icon = models.ImageField(
        db_column="icon",
        verbose_name=_("icon"),
        help_text=_("Event type icon"),
        upload_to="images/event_types/",
        blank=True,
        null=True,
    )

    term_types = models.ManyToManyField(
        TermType,
        db_column="term_types",
        verbose_name=_("term types"),
        help_text=_("Valid term types with which to label this type " "of events"),
        blank=True,
    )

    should_imply = models.ManyToManyField(
        Term,
        db_column="should_imply",
        verbose_name="should imply",
        help_text=_(
            "Terms that should be implied (if meaningful) by "
            "any terms used to describe this event type."
        ),
        blank=True,
    )

    restrict_annotation_types = models.BooleanField(
        db_column="restrict_annotation_types",
        verbose_name=_("restrict annotation types"),
        help_text=_(
            "Flag indicating whether to restrict annotation "
            "types apt for this event type"
        ),
        default=False,
        blank=False,
        null=False,
    )

    annotation_types = models.ManyToManyField(
        "AnnotationType",
        verbose_name=_("annotation types"),
        help_text=_("Valid annotation types for this event type"),
        blank=True,
    )

    item_types = models.ManyToManyField(
        ItemType,
        db_column="item_types",
        verbose_name=_("item types"),
        help_text=_("Types of items in which this event can occur"),
        blank=True,
    )

    class Meta:
        verbose_name = _("Event Type")
        verbose_name_plural = _("Event Types")

        ordering = ["name"]

    def __str__(self):
        return self.name

    def validate_term_type(self, term_type):
        if not self.term_types.filter(pk=term_type.pk).exists():
            msg = _(
                "Term type %(term_type)s is invalid for event " "type %(event_type)s"
            )
            params = dict(term_type=str(term_type), event_type=str(self))
            raise ValidationError(msg, params=params)

    def validate_term(self, term):
        for implication in self.should_imply.all():
            if term.entails(implication):
                continue

            msg = _(
                "Only terms that entail %(implication)s can be used "
                "to describe events of type %(event_type)s. Term %(term)s "
                "does not satisfy this constraint."
            )
            params = dict(implication=implication, event_type=self, term=term)
            raise ValidationError(msg % params)

    def validate_annotation_type(self, annotation_type):
        if not self.restrict_annotation_types:
            return

        if not self.annotation_types.filter(pk=annotation_type.pk).exists():
            msg = _(
                "Annotation type %(annotation_type)s not valid for event "
                "of type %(event_type)s"
            )
            params = dict(annotation_type=str(annotation_type), event_type=str(self))
            raise ValidationError(msg % params)

    def validate_item_type(self, item_type):
        if not self.item_types.filter(pk=item_type.pk).exists():
            msg = _(
                "Event type %(event_type)s is not valid in items of "
                "type %(item_type)s"
            )
            params = dict(item_type=str(item_type), event_type=str(self))
            raise ValidationError(msg % params)
