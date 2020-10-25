from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaAdmin
from selia_visualizers.models import VisualizerModule


class ModuleInline(admin.TabularInline):
    extra = 0

    model = VisualizerModule

    verbose_name_plural = _('Module')

    verbose_name = _('Module')



class ModuleFilter(admin.SimpleListFilter):
    title = _('has module')

    parameter_name = 'module'

    def lookups(self, request, model_admin):
        return (
            ('yes', _('yes')),
            ('no', _('no')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(visualizermodule__isnull=False)

        if self.value() == 'no':
            return queryset.filter(visualizermodule__isnull=True)


def has_module(obj):
    try:
        obj.visualizermodule
        return True

    except ObjectDoesNotExist:
        return False
has_module.boolean = True


class VisualizerVersionAdmin(IrekuaAdmin):
    search_fields = [
        'visualizer__name',
        'version'
    ]

    list_display = (
        'id',
        '__str__',
        'visualizer',
        'version',
        'created_on',
        has_module,
    )

    list_display_links = (
        'id',
        '__str__',
    )

    list_filter = (
        'visualizer',
        'version',
        'created_on',
        ModuleFilter,
    )

    fieldsets = (
        (None, {
            'fields': (
                ('visualizer', 'version'),
                ('created_on',),
            )
        }),
        ('Configuration', {
            'fields': ('configuration_schema',),
        }),
    )

    inlines = [
        ModuleInline,
    ]
