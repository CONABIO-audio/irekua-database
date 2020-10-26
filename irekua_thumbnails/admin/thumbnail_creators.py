from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaAdmin
from irekua_thumbnails.models import ThumbnailCreator


class ItemTypeInline(admin.TabularInline):
    extra = 0

    model = ThumbnailCreator.item_types.through

    autocomplete_fields = [
        'item_type',
    ]

    verbose_name = _('Item Type')

    verbose_name_plural = _('Item Types')


class ThumbnailCreatorAdmin(IrekuaAdmin):
    search_fields = [
        'name',
        'item_types__name',
    ]

    list_display = [
        'id',
        '__str__',
        'created_on',
    ]

    list_display_links = [
        'id',
        '__str__'
    ]

    fieldsets = (
        (None, {
            'fields': (
                ('name', 'python_file'),
            )
        }),
    )

    inlines = [
        ItemTypeInline,
    ]
