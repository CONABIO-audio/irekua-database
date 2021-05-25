from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBaseUser


class TermSuggestion(IrekuaModelBaseUser):
    term_type = models.ForeignKey(
        "TermType",
        on_delete=models.CASCADE,
        db_column="term_type",
        verbose_name=_("term type"),
        help_text=_("Type of term"),
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

    description = models.TextField(
        db_column="description",
        verbose_name=_("description"),
        help_text=_("Description of term"),
        blank=True,
    )

    metadata = models.JSONField(
        blank=True,
        db_column="metadata",
        verbose_name=_("metadata"),
        help_text=_("Metadata associated to term"),
        null=True,
    )

    class Meta:
        ordering = ["-created_on"]
        verbose_name = _("Term Suggestion")
        verbose_name = _("Term Suggestions")

    def __str__(self):
        msg = _("%(term_type)s: %(value)s")
        params = dict(term_type=str(self.term_type), value=self.value)
        return msg % params

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)

        # Check that term type is of the categorical class. It does not
        # make sense to suggest terms of other class.
        self.clean_is_categorical()

        # Check that metadata is valid for this term type
        self.clean_valid_metadata()

    def clean_is_categorical(self):
        #  pylint: disable=no-member
        if not self.term_type.is_categorical:
            msg = _(
                "Cannot create a term suggestion for a non-categorical term"
            )
            raise ValidationError({"term_type": msg})

    def clean_valid_metadata(self):
        try:
            #  pylint: disable=no-member
            self.term_type.validate_metadata(self.metadata)

        except ValidationError as error:
            raise ValidationError({"metadata": error}) from error
