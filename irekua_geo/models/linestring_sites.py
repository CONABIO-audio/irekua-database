from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from .sites import Site


class LineStringSite(Site):
    geometry = models.LineStringField(
        blank=False,
        null=False,
        db_column="geometry",
        verbose_name=_("geometry"),
        help_text=_("LineString geometry of site"),
    )

    class Meta:
        verbose_name = _("LineString Site")

        verbose_name_plural = _("LineString Sites")

        ordering = ["-created_on"]
