from django.contrib import admin

from irekua_database import models
from irekua_database.admin import types
from irekua_database.admin.terms import TermAdmin
from irekua_database.admin.terms import EntailmentAdmin
from irekua_database.admin.terms import TagAdmin
from irekua_database.admin.user import UserAdmin
from irekua_database.admin.item import ItemAdmin
from irekua_database.admin.sampling_events import SamplingEventAdmin
from irekua_database.admin.sampling_events import SamplingEventDeviceAdmin
from irekua_database.admin.data_collections import CollectionAdmin


# TODO: Remove Annotation Tool models when migration is complete
@admin.register(
    models.Annotation,
    # models.AnnotationTool,
    models.AnnotationVote,
    models.CollectionDevice,
    models.CollectionSite,
    models.CollectionUser,
    models.Device,
    models.DeviceBrand,
    models.Institution,
    models.Licence,
    models.Locality,
    models.MetaCollection,
    models.PhysicalDevice,
    models.SecondaryItem,
    models.Site,
    models.SiteDescriptor,
    models.Source,
    models.Synonym,
    models.SynonymSuggestion,
    models.TermSuggestion,
    models.Visualizer,
)
class DatabaseAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Term, TermAdmin)
admin.site.register(models.Entailment, EntailmentAdmin)
admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.SamplingEvent, SamplingEventAdmin)
admin.site.register(models.SamplingEventDevice, SamplingEventDeviceAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Collection, CollectionAdmin)

admin.site.register(models.CollectionType, types.CollectionTypeAdmin)
admin.site.register(models.EventType, types.EventTypeAdmin)
admin.site.register(models.TermType, types.TermTypeAdmin)
admin.site.register(models.SiteType, types.SiteTypeAdmin)
admin.site.register(models.AnnotationType, types.AnnotationTypeAdmin)
admin.site.register(models.ItemType, types.ItemTypeAdmin)
admin.site.register(models.DeviceType, types.DeviceTypeAdmin)
admin.site.register(models.LicenceType, types.LicenceTypeAdmin)
admin.site.register(models.SamplingEventType, types.SamplingEventTypeAdmin)
admin.site.register(models.Role, types.RoleAdmin)
admin.site.register(models.EntailmentType, types.EntailmentTypeAdmin)
admin.site.register(models.LocalityType, types.LocalityTypeAdmin)
admin.site.register(models.SiteDescriptorType, types.SiteDescriptorTypeAdmin)
admin.site.register(models.MimeType, types.MimeTypeAdmin)
