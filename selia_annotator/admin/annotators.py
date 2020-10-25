from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from selia_annotator import models


class VersionsInline(admin.TabularInline):
    extra = 0
    model = models.AnnotatorVersion
    verbose_name = _('Version')
    verbose_name_plural = _('Versions')


class ModulesInline(admin.TabularInline):
    classes = ('collapse', )
    extra = 0
    model = models.AnnotatorModule
    verbose_name = _('Javascript Module')
    verbose_name_plural = _('Javascript Modules')


class AnnotatorAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'

    search_fields = [
        'name',
        'annotation_type__name',
    ]

    list_display = [
        'id',
        'name',
        'annotation_type',
        'created_on',
    ]

    list_display_links = [
        'id',
        'name',
    ]

    autocomplete_fields = [
        'annotation_type',
    ]

    list_filter = [
        'annotation_type',
    ]

    readonly_fields = (
        'created_on',
        'modified_on',
    )

    fieldsets = (
        (None, {
            'fields': (
                ('name', 'annotation_type',),
                ('website', 'logo',),
            )
        }),
        ('Creation', {
            'fields': (
                ('created_on', 'modified_on'),
            )
        })
    )

    inlines = [
        VersionsInline,
        ModulesInline,
    ]
