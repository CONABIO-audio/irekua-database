from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_database.models import ItemType


class MimeTypesInline(admin.TabularInline):
    extra = 0
    model = ItemType.mime_types.through
    autocomplete_fields = ('mimetype',)
    verbose_name = _('Mime type')
    verbose_name_plural = _('Mime types')
    classes = ('collapse', )


class EventTypesInline(admin.TabularInline):
    extra = 0
    model = ItemType.event_types.through
    autocomplete_fields = ('eventtype',)
    verbose_name = _('Event type')
    verbose_name_plural = _('Event types')
    classes = ('collapse', )


class ItemTypeAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('id', 'name', 'created_on')
    list_display_links = ('id', 'name')


    fieldsets = (
        (None, {
            'fields': (
                ('name', 'icon'),
                'description'
            ),
        }),
    )

    inlines = [
        MimeTypesInline,
        EventTypesInline,
    ]
