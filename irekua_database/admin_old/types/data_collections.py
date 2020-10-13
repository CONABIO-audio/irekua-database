from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_database.models import CollectionType


class SiteTypeInline(admin.TabularInline):
    extra = 0
    model = CollectionType.site_types.through
    autocomplete_fields = ('sitetype',)
    verbose_name = _('Site type')
    verbose_name_plural = _('Site types')
    classes = ('collapse', )


class ItemTypeInline(admin.TabularInline):
    extra = 0
    model = CollectionType.item_types.through
    autocomplete_fields = ('item_type',)
    verbose_name = _('Item type')
    verbose_name_plural = _('Item types')
    classes = ('collapse', )


class AnnotationTypeInline(admin.TabularInline):
    extra = 0
    model = CollectionType.annotation_types.through
    autocomplete_fields = ('annotationtype',)
    verbose_name = _('Annotation type')
    verbose_name_plural = _('Annotation types')
    classes = ('collapse', )


class LicenceTypeInline(admin.TabularInline):
    extra = 0
    model = CollectionType.licence_types.through
    autocomplete_fields = ('licencetype',)
    verbose_name = _('Licence type')
    verbose_name_plural = _('Licence types')
    classes = ('collapse', )


class DeviceTypeInline(admin.TabularInline):
    extra = 0
    model = CollectionType.device_types.through
    autocomplete_fields = ('device_type',)
    verbose_name = _('Device type')
    verbose_name_plural = _('Device types')
    classes = ('collapse', )


class EventTypeInline(admin.TabularInline):
    extra = 0
    model = CollectionType.event_types.through
    autocomplete_fields = ('eventtype',)
    verbose_name = _('Event type')
    verbose_name_plural = _('Event types')
    classes = ('collapse', )


class SamplingEventTypeInline(admin.TabularInline):
    extra = 0
    model = CollectionType.sampling_event_types.through
    autocomplete_fields = ('samplingeventtype',)
    verbose_name = _('Sampling event type')
    verbose_name_plural = _('Sampling event types')
    classes = ('collapse', )


class RoleInline(admin.TabularInline):
    extra = 0
    model = CollectionType.roles.through
    autocomplete_fields = ('role',)
    verbose_name = _('Role')
    verbose_name_plural = _('Roles')
    classes = ('collapse', )


class CollectionTypeAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    search_fields = ('name', )
    list_filter = (
        'name',
        'anyone_can_create',
        'restrict_site_types',
        'restrict_annotation_types',
        'restrict_item_types',
        'restrict_licence_types',
        'restrict_device_types',
        'restrict_event_types',
        'restrict_sampling_event_types',
    )
    list_display = (
        'id',
        'name',
        'anyone_can_create',
        'restrict_site_types',
        'restrict_annotation_types',
        'restrict_item_types',
        'restrict_licence_types',
        'restrict_device_types',
        'restrict_event_types',
        'restrict_sampling_event_types',
    )
    autocomplete_fields = (
        'site_types',
        'annotation_types',
        'licence_types',
        'event_types',
        'sampling_event_types',
        'item_types',
        'device_types',
        'roles',
        'administrators',
    )

    fieldsets = (
        (None, {
            'fields': (
                ('name', 'logo'),
                'description'
            ),
        }),
        ('Metadata', {
            'classes': ('collapse', ),
            'fields': ('metadata_schema', ),
        }),
        ('Admin and Permissions', {
            'classes': ('collapse', ),
            'fields': (('administrators', 'anyone_can_create'),)
        }),
        ('Restrictions', {
            'classes': ('collapse', ),
            'fields': (
                (
                    'restrict_site_types',
                    'restrict_device_types',
                    'restrict_sampling_event_types'
                ),
                ('restrict_item_types', 'restrict_licence_types'),
                ('restrict_event_types', 'restrict_annotation_types'),
            ),
        }),
    )

    inlines = [
        LicenceTypeInline,
        DeviceTypeInline,
        SiteTypeInline,
        SamplingEventTypeInline,
        ItemTypeInline,
        EventTypeInline,
        AnnotationTypeInline,
        RoleInline,
    ]
