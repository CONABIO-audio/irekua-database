from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaUserAdmin
from irekua_organisms.models import OrganismCapture


class LabelsInline(admin.TabularInline):
    extra = 0

    model = OrganismCapture.labels.through

    verbose_name = _('Label')

    verbose_name_plural = _('Labels')

    autocomplete_fields = ['term']


class OrganismCaptureAdmin(IrekuaUserAdmin):
    date_hierarchy = 'created_on'

    search_fields = [
        'organism__name'
        'organism__organism_type__name',
        'deployment__collection_device__collection_name',
        'organism__collection__collection_name',
    ]

    list_display = (
        'id',
        '__str__',
        'collection',
        'sampling_event',
        'deployment',
        'organism',
        'organism_capture_type',
        'created_on',
        'created_by',
    )

    list_display_links = (
        'id',
        '__str__',
    )

    list_filter = (
        'organism_capture_type',
        'deployment',
        'organism',
    )

    autocomplete_fields = (
        'labels',
        'deployment',
        'organism_capture_type',
        'organism'
    )

    fieldsets = (
        (None, {
            'fields': (
                ('organism_capture_type', 'deployment'),
                ('organism'),
            )
        }),
        (_('Additional metadata'), {
            'fields': (
                ('metadata', 'collection_metadata'),
            ),
        }),
        (_('Descriptors'), {
            'classes': ('collapse',),
            'fields': ('labels',),
        }),
    )

    inlines = [
        LabelsInline,
    ]
