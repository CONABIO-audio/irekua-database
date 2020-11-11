from django.contrib import admin

from irekua_geo import models

from .linestring_sites import LineStringSiteAdmin
from .localities import LocalityAdmin
from .locality_types import LocalityTypeAdmin
from .multilinestring_sites import MultiLineStringSiteAdmin
from .multipoint_sites import MultiPointSiteAdmin
from .multipolygon_sites import MultiPolygonSiteAdmin
from .point_sites import PointSiteAdmin
from .polygon_sites import PolygonSiteAdmin
from .site_descriptor_types import SiteDescriptorTypeAdmin
from .site_descriptors import SiteDescriptorAdmin
from .site_types import SiteTypeAdmin
from .sites import SiteAdmin


admin.site.register(models.LineStringSite, LineStringSiteAdmin)
admin.site.register(models.Locality, LocalityAdmin)
admin.site.register(models.LocalityType, LocalityTypeAdmin)
admin.site.register(models.MultiLineStringSite, MultiLineStringSiteAdmin)
admin.site.register(models.MultiPointSite, MultiPointSiteAdmin)
admin.site.register(models.MultiPolygonSite, MultiPolygonSiteAdmin)
admin.site.register(models.PointSite, PointSiteAdmin)
admin.site.register(models.PolygonSite, PolygonSiteAdmin)
admin.site.register(models.Site, SiteAdmin)
admin.site.register(models.SiteDescriptor, SiteDescriptorAdmin)
admin.site.register(models.SiteDescriptorType, SiteDescriptorTypeAdmin)
admin.site.register(models.SiteType, SiteTypeAdmin)
