from django.utils.translation import gettext_lazy as _

from .sites import SiteAdmin


class LineStringSiteAdmin(SiteAdmin):
    fieldsets = (
        *SiteAdmin.fieldsets,
        (_("Geometry"), {"fields": ("geometry",)}),
    )
