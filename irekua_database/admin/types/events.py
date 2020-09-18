from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_database.models import EventType


class TermTypesInline(admin.TabularInline):
    extra = 0
    model = EventType.term_types.through
    autocomplete_fields = ('termtype',)
    verbose_name = _('Term type')
    verbose_name_plural = _('Term types')
    classes = ('collapse', )


class ShouldImplyInline(admin.TabularInline):
    extra = 0
    model = EventType.should_imply.through
    autocomplete_fields = ('term',)
    verbose_name = _('Should imply')
    verbose_name_plural = _('Should imply')
    classes = ('collapse', )


class EventTypeAdmin(admin.ModelAdmin):
    search_fields = ['name']
    autocomplete_fields = ['should_imply']
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
        TermTypesInline,
        ShouldImplyInline,
    ]
