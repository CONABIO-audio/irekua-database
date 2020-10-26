from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaAdmin

from irekua_items.models import MediaInfoExtractor


class ExtractorInline(admin.TabularInline):
    extra = 0

    model = MediaInfoExtractor

    verbose_name = _('Extractor')

    verbose_name = _('Extractors')


class MediaInfoTypeAdmin(IrekuaAdmin):
    search_fields = [
        'name',
    ]

    list_display = [
        'id',
        '__str__',
        'created_on',
    ]

    list_display_links = [
        'id',
        '__str__',
    ]

    fieldsets = (
        (None, {
            'fields': (
                ('name', 'media_info_schema'),
                'description',
            ),
        }),
    )

    inlines = [
        ExtractorInline,
    ]
