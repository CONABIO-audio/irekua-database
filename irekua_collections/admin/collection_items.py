from django.utils.translation import gettext_lazy as _

from irekua_items.admin.items import ItemAdmin


class CollectionItemAdmin(ItemAdmin):
    search_fields = [
        'collection__name',
        *ItemAdmin.search_fields,
    ]

    list_display = [
        'id',
        '__str__',
        'item_type',
        'licence',
        'collection',
        'filesize',
        'captured_on',
        'created_by',
        'created_on',
    ]

    list_filter = [
        'collection',
        *ItemAdmin.list_filter,
    ]

    autocomplete_fields = [
        'collection',
        *ItemAdmin.autocomplete_fields,
    ]

    fieldsets = (
        (None, {
            'fields': (
                'collection',
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
        return queryset.exclude(deviceitem__isnull=False, siteitem__isnull=False)

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return self.filter_queryset(queryset)
