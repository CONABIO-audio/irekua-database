from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .data_collections import CollectionTypeAdmin
from .events import EventTypeAdmin
from .devices import DeviceTypeAdmin
from .items import ItemTypeAdmin
from .sites import SiteTypeAdmin
from .sampling_events import SamplingEventTypeAdmin


class AnnotationTypeAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('id', 'name', 'created_on')
    list_display_links = ('id', 'name')

    fieldsets = (
        (None, {
            'fields': (
                ('name', 'icon'),
                'description'
            ),
        }),
        ('Schema', {
            'classes': ('collapse', ),
            'fields': ('annotation_schema', ),
        }),
    )


class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']


class LicenceTypeAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('id', 'name', 'years_valid_for', 'can_view', 'created_on')
    list_display_links = ('id', 'name')
    list_filter = (
        'can_view',
        'can_download',
        'can_view_annotations',
        'can_annotate',
        'can_vote_annotations')

    fieldsets = (
        (None, {
            'fields': (
                ('name', 'icon'),
                'description'
            ),
        }),
        ('Template and additional metadata', {
            'classes': ('collapse', ),
            'fields': ('document_template', 'metadata_schema'),
        }),
        ('Permissions', {
            'classes': ('collapse', ),
            'fields': (
                ('years_valid_for',),
                ('can_view', 'can_download', 'can_view_annotations', 'can_annotate', 'can_vote_annotations'),
            )
        }),
    )


class LocalityTypeAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('id', 'name', 'publication_date')
    list_display_links = ('id', 'name')

    fieldsets = (
        (None, {
            'fields': ('name', 'description'),
        }),
        ('Source', {
            'classes': ('collapse', ),
            'fields': ('source', 'original_datum', 'publication_date'),
        }),
        ('Additional metadata', {
            'classes': ('collapse', ),
            'fields': ('metadata_schema',)
        }),
    )


class MimeTypeAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('id', 'mime_type', 'created_on')
    list_display_links = ('id', 'mime_type')


class SiteDescriptorTypeAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('id', 'name', 'created_on')
    list_display_links = ('id', 'name')

    fieldsets = (
        (None, {
            'fields': (
                ('name', 'icon'),
                'description'
            ),
        }),
        ('Source', {
            'classes': ('collapse', ),
            'fields': ('source', 'metadata'),
        }),
        ('Additional metadata', {
            'classes': ('collapse', ),
            'fields': ('metadata_schema',)
        }),
    )


class RoleAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('id', 'name', 'created_on')
    list_display_links = ('id', 'name')

    fieldsets = (
        (None, {
            'fields': (
                ('name', 'icon'),
                'description',
            ),
        }),
        ('Permissions', {
            'classes': ('collapse', ),
            'fields': ('permissions',)
        }),
    )
