from django.contrib import admin

from irekua_collections import models

from .collection_devices import CollectionDeviceAdmin
from .collection_items import CollectionItemAdmin
from .collection_licences import CollectionLicenceAdmin
from .collection_sites import CollectionSiteAdmin
from .collection_types import CollectionTypeAdmin
from .collection_users import CollectionUserAdmin
from .data_collections import CollectionAdmin
from .deployment_items import DeploymentItemAdmin
from .deployments import DeploymentAdmin
from .sampling_event_items import SamplingEventItemAdmin
from .sampling_events import SamplingEventAdmin


admin.site.register(models.CollectionDevice, CollectionDeviceAdmin)
admin.site.register(models.CollectionItem, CollectionItemAdmin)
admin.site.register(models.CollectionLicence, CollectionLicenceAdmin)
admin.site.register(models.CollectionSite, CollectionSiteAdmin)
admin.site.register(models.CollectionType, CollectionTypeAdmin)
admin.site.register(models.CollectionUser, CollectionUserAdmin)
admin.site.register(models.Collection, CollectionAdmin)
admin.site.register(models.DeploymentItem, DeploymentItemAdmin)
admin.site.register(models.Deployment, DeploymentAdmin)
admin.site.register(models.SamplingEventItem, SamplingEventItemAdmin)
admin.site.register(models.SamplingEvent, SamplingEventAdmin)
