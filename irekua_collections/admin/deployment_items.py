from django.utils.translation import gettext_lazy as _

from .sampling_event_items import SamplingEventItemAdmin


class DeploymentItemAdmin(SamplingEventItemAdmin):
    search_fields = [
        'deployment__deployment_type__name',
        'collection_device__collection_name',
        'collection_device__physical_device__device__device_type__name',
        *SamplingEventItemAdmin.search_fields,
    ]

    list_display = [
        'id',
        '__str__',
        'collection',
        'collection_site',
        'collection_device',
        'sampling_event',
        'deployment',
        'item_type',
        'filesize',
        'licence',
        'captured_on',
        'created_by',
        'created_on',
    ]

    list_filter = [
        'deployment__deployment_type',
        'collection_device__physical_device__device__device_type',
        *SamplingEventItemAdmin.list_filter,
    ]

    autocomplete_fields = [
        'deployment',
        'collection_device',
        *SamplingEventItemAdmin.autocomplete_fields,
    ]

    fieldsets = (
        (None, {
            'fields': (
                'deployment',
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
        return queryset
