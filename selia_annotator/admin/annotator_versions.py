from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaAdmin
from selia_annotator.models import AnnotatorModule


class ModuleInline(admin.TabularInline):
    extra = 0

    model = AnnotatorModule

    fk_name = 'annotatorversion_ptr'

    verbose_name_plural = _('Module')

    verbose_name = _('Module')

    fields = [
        'javascript_file',
        'is_active',
    ]


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
            return queryset.filter(annotatormodule__isnull=False)

        if self.value() == 'no':
            return queryset.filter(annotatormodule__isnull=True)


def has_module(obj):
    try:
        obj.annotatormodule
        return True

    except ObjectDoesNotExist:
        return False
has_module.boolean = True


class AnnotatorVersionAdmin(IrekuaAdmin):
    search_fields = [
        'annotator__name',
        'version']

    list_display = [
        'id',
        '__str__',
        'annotator',
        'version',
        has_module,
        'created_on',
    ]

    list_display_links = [
        'id',
        '__str__',
    ]

    autocomplete_fields = [
        'annotator',
    ]

    list_filter = [
        'annotator',
        'annotator__annotation_type',
        ModuleFilter,
    ]

    fieldsets = (
        (None, {
            'fields': (
                ('annotator', 'version'),
            )
        }),
    )

    inlines = [
        ModuleInline,
    ]
