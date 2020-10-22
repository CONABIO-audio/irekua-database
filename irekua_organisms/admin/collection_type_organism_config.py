from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaAdmin
from irekua_organisms.models import CollectionTypeOrganismConfig


class CollectionTypeOrganismTypeInline(admin.TabularInline):
    extra = 0
    model = CollectionTypeOrganismConfig.organism_types.through
    autocomplete_fields = ('organism_type',)
    verbose_name = _('Organism type')
    verbose_name_plural = _('Organism types')


class CollectionTypeOrganismCaptureTypeInline(admin.TabularInline):
    extra = 0
    model = CollectionTypeOrganismConfig.organism_capture_types.through
    autocomplete_fields = ('organism_capture_type',)
    verbose_name = _('Organism capture type')
    verbose_name_plural = _('Organism capture types')


class CollectionTypeOrganismConfigAdmin(IrekuaAdmin):
    search_fields = (
        'collection_type__name',
    )

    list_display = (
        'collection_type',
        'use_organisms',
        'restrict_organism_types',
        'restrict_organism_capture_types',
        'created_on',
    )

    list_display_links = (
        'collection_type',
    )

    list_filter = (
        'use_organisms',
        'restrict_organism_types',
        'restrict_organism_capture_types',
    )

    autocomplete_fields = (
        'collection_type',
    )

    fieldsets = (
        (None, {
            'fields': (
                'collection_type',
                'use_organisms',
            )
        }),
        (_('Restrictions'), {
            'fields': (
                ('restrict_organism_types', 'restrict_organism_capture_types'),
            )
        }),
    )

    inlines = [
        CollectionTypeOrganismTypeInline,
        CollectionTypeOrganismCaptureTypeInline,
    ]
