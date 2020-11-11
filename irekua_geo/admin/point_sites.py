from django.utils.translation import gettext_lazy as _

from .sites import SiteAdmin


class PointSiteAdmin(SiteAdmin):
    fieldsets = (
        *SiteAdmin.fieldsets,
        (
            _("Geometry"),
            {
                "fields": (
                    ("latitude", "longitude", "altitude"),
                    "geometry",
                )
            },
        ),
    )
