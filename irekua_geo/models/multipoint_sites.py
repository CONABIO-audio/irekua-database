from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from .sites import Site


class MultiPointSite(Site):
    geometry = models.MultiPointField(
        blank=False,
        null=False,
        db_column="geometry",
        verbose_name=_("geometry"),
        help_text=_("MultiPoint geometry of site"),
    )

    class Meta:
        verbose_name = _("MultiPoint Site")

        verbose_name_plural = _("MultiPoint Sites")

        ordering = ["-created_on"]
