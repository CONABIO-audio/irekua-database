from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaAdmin


class CollectionTypeAdmin(IrekuaAdmin):
    search_fields = [
        'name',
    ]

    list_display = [
        'id',
        'name',
        'anyone_can_create',
        'created_on'
    ]

    list_display_links = [
        'id',
        'name',
    ]

    fieldsets = (
        (None, {
            'fields': ('name',),
        }),
    )
