from django.contrib import admin

from irekua_types import models

from .device_types import DeviceTypeAdmin
from .locality_types import LocalityTypeAdmin
from .mime_types import MimeTypeAdmin
from .site_descriptor_types import SiteDescriptorTypeAdmin
from .site_types import SiteTypeAdmin


admin.site.register(models.DeviceType, DeviceTypeAdmin)
admin.site.register(models.LocalityType, LocalityTypeAdmin)
admin.site.register(models.MimeType, MimeTypeAdmin)
admin.site.register(models.SiteDescriptorType, SiteDescriptorTypeAdmin)
admin.site.register(models.SiteType, SiteTypeAdmin)
