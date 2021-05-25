from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase


class Term(IrekuaModelBase):
    term_type = models.ForeignKey(
        "TermType",
        on_delete=models.CASCADE,
        db_column="term_type",
        verbose_name=_("term type"),
        help_text=_("Type of term"),
        limit_choices_to={"is_categorical": True},
        blank=False,
        null=False,
    )

    value = models.CharField(
        max_length=128,
        db_column="value",
        verbose_name=_("value"),
        help_text=_("Value of term"),
        blank=False,
    )

    scope = models.CharField(
        max_length=128,
        db_column="scope",
        verbose_name=_("scope"),
        help_text=_("Scope of term. Use for disambiguation."),
        blank=True,
    )

    description = models.TextField(
        db_column="description",
        verbose_name=_("description"),
        help_text=_("Description of term"),
        blank=True,
    )

    url = models.URLField(
        db_column="url",
        verbose_name=_("term url"),
        help_text=_("URL for term description"),
        blank=True,
    )

    metadata = models.JSONField(
        db_column="metadata",
        verbose_name=_("metadata"),
        help_text=_("Metadata associated to term"),
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["term_type", "value"]
        verbose_name = _("Term")
        verbose_name_plural = _("Terms")
        unique_together = ("term_type", "value", "scope")

    def __str__(self):
        msg = "{term_type}: {value}".format(
            term_type=self.term_type, value=self.value
        )
        return msg

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)

        #  Check that term value is consistent with the declared type
        # (categorical/numeric/boolean/integer) of the term type.
        self.clean_validate_value()

        # Check that metadata is valid for term type
        self.clean_valid_metadata()

    def clean_validate_value(self):
        try:
            # pylint: disable=no-member
            self.term_type.validate_value(self.value)

        except ValidationError as error:
            raise ValidationError({"value": error}) from error

    def clean_valid_metadata(self):
        try:
            # pylint: disable=no-member
            self.term_type.validate_metadata(self.metadata)

        except ValidationError as error:
            raise ValidationError({"metadata": error}) from error

    def entails(self, term):
        return self.entailment_source.filter(target=term).exists()

    def entailments(self):
        return Term.objects.filter(entailment_target__source=self)

    def synonyms(self):
        return Term.objects.filter(synonym_target__source=self)
