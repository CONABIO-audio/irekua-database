from django.utils.translation import gettext_lazy as _

from .site_items import SiteItemAdmin


class SamplingEventItemAdmin(SiteItemAdmin):
    list_display = [
        'id',
        '__str__',
        'item_type',
        'licence',
        'collection',
        'collection_site',
        'sampling_event',
        'filesize',
        'captured_on',
        'created_by',
        'created_on',
    ]

    list_filter = [
        'sampling_event__sampling_event_type',
        *SiteItemAdmin.list_filter,
    ]

    autocomplete_fields = [
        'sampling_event',
        *SiteItemAdmin.autocomplete_fields,
    ]

    fieldsets = (
        (None, {
            'fields': (
                'sampling_event',
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
        return queryset.filter(deploymentitem__isnull=True)
