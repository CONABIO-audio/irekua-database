from django.contrib import admin

from irekua_devices import models


from .brands import DeviceBrandAdmin
from .devices import DeviceAdmin
from .physical_devices import PhysicalDeviceAdmin


admin.site.register(models.DeviceBrand, DeviceBrandAdmin)
admin.site.register(models.Device, DeviceAdmin)
admin.site.register(models.PhysicalDevice, PhysicalDeviceAdmin)
