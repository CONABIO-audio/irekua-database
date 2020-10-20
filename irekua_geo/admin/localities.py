from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaAdmin
from irekua_geo.models import Locality


class SupersetInline(admin.TabularInline):
    extra = 0

    model = Locality.is_part_of.through

    verbose_name = _('Superset')

    verbose_name_plural = _('Supersets')

    autocomplete_fields = [
        'to_locality',
    ]

    fk_name = 'from_locality'


class LocalityAdmin(IrekuaAdmin):
    search_fields = [
        'id',
        'name',
    ]

    list_display = [
        'id',
        'name',
        'locality_type',
        'created_on',
    ]

    list_display_links = [
        'id',
        'name',
    ]

    list_filter = [
        'locality_type',
    ]

    autocomplete_fields = [
        'locality_type',
    ]

    fieldsets = (
        (None, {
            'fields': (
                ('name','locality_type'),
                'description',
                'geometry',
            )
        }),
        (_('Additional Metadata'), {
            'fields': (
                ('metadata',),
            )
        })
    )

    inlines = [
        SupersetInline,
    ]
