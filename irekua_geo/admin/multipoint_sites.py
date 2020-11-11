from django.utils.translation import gettext_lazy as _

from .sites import SiteAdmin


class MultiPointSiteAdmin(SiteAdmin):
    fieldsets = (*SiteAdmin.fieldsets, (_("Geometry"), {"fields": ("geometry",)}))
