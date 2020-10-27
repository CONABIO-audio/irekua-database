from django.utils.translation import gettext_lazy as _

from .collection_items import CollectionItemAdmin


class SiteItemAdmin(CollectionItemAdmin):
    search_fields = [
        'collection_site__collection_name',
        'collection_site__site_type__name',
        *CollectionItemAdmin.search_fields,
    ]

    list_display = [
        'id',
        '__str__',
        'item_type',
        'licence',
        'collection',
        'collection_site',
        'filesize',
        'captured_on',
        'created_by',
        'created_on',
    ]

    list_filter = [
        'collection_site__site_type',
        *CollectionItemAdmin.list_filter,
    ]

    autocomplete_fields = [
        'collection_site',
        *CollectionItemAdmin.autocomplete_fields,
    ]

    fieldsets = (
        (None, {
            'fields': (
                'collection_site',
                ('item_type', 'licence'),
                'item_file',
            )
        }),
        (_('Item Info'), {
            'fields': (
                ('hash', 'filesize'),
                'media_info',
            )
        }),
        (_('Captured on'), {
            'fields': (
                ('captured_on', 'captured_on_timezone'),
                ('captured_on_year', 'captured_on_month', 'captured_on_day'),
                ('captured_on_hour', 'captured_on_minute', 'captured_on_second'),
            )
        }),
        (_('Additional Metadata'), {
            'fields': (
                ('metadata', 'collection_metadata'),
            ),
        }),
        (_('Source'), {
            'classes': ('collapse', ),
            'fields': (
                ('source', 'source_foreign_key'),
            )
        })
    )

    def filter_queryset(self, queryset):
        return queryset.filter(samplingeventitem__isnull=True)
