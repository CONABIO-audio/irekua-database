from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaAdmin
from irekua_devices.models import DeviceType


class MimeTypesInline(admin.TabularInline):
    extra = 0
    model = DeviceType.mime_types.through
    autocomplete_fields = ('mimetype',)
    verbose_name = _('Mime type')
    verbose_name_plural = _('Mime types')
    classes = ('collapse', )


class DeviceTypeAdmin(IrekuaAdmin):
    search_fields = [
        'name',
        'mime_types__name'
    ]

    list_display = [
        'id',
        'name',
        'created_on'
    ]

    list_display_links = [
        'id',
        'name',
    ]

    fieldsets = (
        (None, {
            'fields': (
                ('name', 'icon'),
                'description'
            ),
        }),
    )

    inlines = [
        MimeTypesInline
    ]
