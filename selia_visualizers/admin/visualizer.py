from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from selia_visualizers import models


class ItemTypeInline(admin.TabularInline):
    extra = 0
    model = models.Visualizer.item_types.through
    autocomplete_fields = ('item_type',)
    verbose_name = _('Item type')
    verbose_name_plural = _('Item types')


class VisualizerAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    search_fields = ['name', 'description']
    list_display = (
        'id',
        'name',
        'website',
        'created_on',
    )
    readonly_fields = ('created_on',)
    list_display_links = ('id', 'name',)
    list_filter = (
        'name',
        'created_on',)

    fieldsets = (
        (None, {
            'fields': (
                ('name', 'website'),
                ('description',),
                ('created_on',),
            )
        }),
        ('Configuration', {
            'classes': ('collapse',),
            'fields': ('configuration_schema',),
        }),
    )

    inlines = [
        ItemTypeInline,
    ]
