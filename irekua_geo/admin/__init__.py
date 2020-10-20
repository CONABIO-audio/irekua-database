from django.contrib import admin

from irekua_geo import models


from .site_descriptors import SiteDescriptorAdmin
from .localities import LocalityAdmin
from .sites import SiteAdmin


admin.site.register(models.SiteDescriptor, SiteDescriptorAdmin)
admin.site.register(models.Locality, LocalityAdmin)
admin.site.register(models.Site, SiteAdmin)
