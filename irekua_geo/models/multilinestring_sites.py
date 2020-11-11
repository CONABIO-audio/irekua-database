from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from .sites import Site


class MultiLineStringSite(Site):
    geometry = models.MultiLineStringField(
        blank=False,
        null=False,
        db_column="geometry",
        verbose_name=_("geometry"),
        help_text=_("MultiLine geometry of site"),
    )

    class Meta:
        verbose_name = _("MultiLineString Site")

        verbose_name_plural = _("MultiLineString Sites")

        ordering = ["-created_on"]
