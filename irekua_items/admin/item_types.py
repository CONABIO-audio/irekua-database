from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_items.models import ItemType


class MimeTypesInline(admin.TabularInline):
    extra = 0

    model = ItemType.mime_types.through

    autocomplete_fields = ('mimetype',)

    verbose_name = _('Mime type')

    verbose_name_plural = _('Mime types')


class ItemTypeAdmin(admin.ModelAdmin):
    search_fields = [
        'name'
    ]

    list_display = (
        'id',
        'name',
        'created_on'
    )

    list_display_links = (
        'id',
        'name'
    )

    autocomplete_fields = [
        'metadata_schema',
        'media_info_type',
    ]

    fieldsets = (
        (None, {
            'fields': (
                ('name', 'icon'),
                'description'
            ),
        }),
        ('Schemas', {
            'fields': (
                'metadata_schema',
                'media_info_type',
            )
        }),
    )

    inlines = [
        MimeTypesInline,
    ]
