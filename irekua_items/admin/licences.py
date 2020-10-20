from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaUserAdmin


class LicenceAdmin(IrekuaUserAdmin):
    search_fields = [
        'licence_type__name',
        'created_on__username',
    ]

    list_display = [
        'id',
        'licence_type',
        'is_active',
        'created_by',
        'created_on',
    ]

    list_display_links = [
        'id',
    ]

    autocomplete_fields = [
        'licence_type',
    ]

    list_filter = [
        'is_active',
    ]

    readonly_fields = [
        *IrekuaUserAdmin.readonly_fields,
        'is_active',
    ]

    fieldsets = (
        (None, {
            'fields': (
                ('licence_type', 'document'),
                'metadata',
            )
        }),
        (_('Active'), {
            'fields': (
                'is_active',
            )
        })
    )
