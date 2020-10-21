from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaUserAdmin
from irekua_collections.models import DeploymentItem


class TagInline(admin.TabularInline):
    extra = 0

    model = DeploymentItem.tags.through

    verbose_name = _('Tag')

    verbose_name_plural = _('Tags')

    autocomplete_fields = [
        'tag',
    ]


class ReadyEventTypeInline(admin.TabularInline):
    extra = 0

    model = DeploymentItem.ready_event_types.through

    verbose_name = _('Ready Event Type')

    verbose_name_plural = _('Ready Event Types')

    autocomplete_fields = [
        'eventtype',
    ]


class DeploymentItemAdmin(IrekuaUserAdmin):
    search_fields = [
        'collection__name',
        'item_type__name',
        'licence__licence_type__name',
        'id',
    ]

    list_display = [
        '__str__',
        'collection',
        'deployment',
        'item_type',
        'filesize',
        'licence',
        'captured_on',
        'created_by',
        'created_on',
    ]

    list_display_links = [
        '__str__',
    ]

    list_filter = [
        'collection',
        'item_type',
        'licence__licence_type',
        'deployment__deployment_type',
        'sampling_event__sampling_event_type',
    ]

    autocomplete_fields = [
        'deployment',
        'item_type',
        'licence',
        'source',
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

    inlines = [
        TagInline,
        ReadyEventTypeInline,
    ]
