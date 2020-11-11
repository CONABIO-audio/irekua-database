from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from .sites import Site


class PolygonSite(Site):
    geometry = models.PolygonField(
        blank=False,
        null=False,
        db_column="geometry",
        verbose_name=_("geometry"),
        help_text=_("Polygon geometry of site"),
    )

    class Meta:
        verbose_name = _("Polygon Site")

        verbose_name_plural = _("Polygon Sites")

        ordering = ["-created_on"]
