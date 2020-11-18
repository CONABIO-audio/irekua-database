from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase
from irekua_annotations.models import AnnotationType


class Annotator(IrekuaModelBase):
    annotation_type = models.ForeignKey(
        AnnotationType,
        on_delete=models.CASCADE,
        db_column="annotation_type_id",
        verbose_name=_("annotation type"),
        help_text=_("Type of annotation this annotator produces"),
    )

    name = models.CharField(
        max_length=64,
        db_column="name",
        unique=True,
        verbose_name=_("name"),
        help_text=_("Name of annotator"),
        blank=False,
    )

    logo = models.ImageField(
        db_column="logo",
        verbose_name=_("logo"),
        help_text=_("Annotator logo"),
        upload_to="images/annotators/",
        blank=True,
        null=True,
    )

    website = models.URLField(
        db_column="website",
        verbose_name=_("website"),
        help_text=_("Annotator website"),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Annotator")

        verbose_name_plural = _("Annotators")

        ordering = ["-created_on"]

    def __str__(self):
        return str(self.name)

    def validate_annotation_type(self, annotation_type):
        if self.annotation_type != annotation_type:
            msg = _(
                "Annotator %(annotator)s does not produce annotations "
                "of type %(annotation_type)s"
            )
            params = dict(annotator=self, annotation_type=annotation_type)
            raise ValidationError(msg % params)
