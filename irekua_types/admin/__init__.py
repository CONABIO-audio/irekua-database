from django.contrib import admin

from irekua_types import models

from .annotation_types import AnnotationTypeAdmin
from .deployment_types import DeploymentTypeAdmin
from .device_types import DeviceTypeAdmin
from .event_types import EventTypeAdmin
from .item_types import ItemTypeAdmin
from .licence_types import LicenceTypeAdmin
from .locality_types import LocalityTypeAdmin
from .mime_types import MimeTypeAdmin
from .sampling_event_types import SamplingEventTypeAdmin
from .site_descriptor_types import SiteDescriptorTypeAdmin
from .site_types import SiteTypeAdmin


admin.site.register(models.AnnotationType, AnnotationTypeAdmin)
admin.site.register(models.DeploymentType, DeploymentTypeAdmin)
admin.site.register(models.DeviceType, DeviceTypeAdmin)
admin.site.register(models.EventType, EventTypeAdmin)
admin.site.register(models.ItemType, ItemTypeAdmin)
admin.site.register(models.LicenceType, LicenceTypeAdmin)
admin.site.register(models.LocalityType, LocalityTypeAdmin)
admin.site.register(models.MimeType, MimeTypeAdmin)
admin.site.register(models.SamplingEventType, SamplingEventTypeAdmin)
admin.site.register(models.SiteDescriptorType, SiteDescriptorTypeAdmin)
admin.site.register(models.SiteType, SiteTypeAdmin)
