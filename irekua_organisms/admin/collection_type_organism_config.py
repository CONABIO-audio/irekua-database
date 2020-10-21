from django.contrib import admin
from django.utils.translation import gettext_lazy as _

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


class CollectionTypeOrganismConfigAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    search_fields = ('collection_type__name',)
    list_display = (
        'collection_type',
        'use_organisms',
    )
    list_filter = (
        'use_organisms',
        'created_on',
    )

    autocomplete_fields = ('collection_type',)
    fields = (
        ('collection_type', 'use_organisms'),
    )

    inlines = [
        CollectionTypeOrganismTypeInline,
        CollectionTypeOrganismCaptureTypeInline,
    ]
