from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from .sites import Site


class MultiPolygonSite(Site):
    geometry = models.MultiPolygonField(
        blank=False,
        null=False,
        db_column="geometry",
        verbose_name=_("geometry"),
        help_text=_("MultiPolygon geometry of site"),
    )

    class Meta:
        verbose_name = _("MultiPolygon Site")

        verbose_name_plural = _("MultiPolygon Sites")

        ordering = ["-created_on"]
