from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_types.models import SiteType


class SiteDescriptorTypeInline(admin.TabularInline):
    extra = 0
    model = SiteType.site_descriptor_types.through
    autocomplete_fields = ('sitedescriptortype',)
    verbose_name = _('Site descriptor type')
    verbose_name_plural = _('Site descriptor types')
    classes = ('collapse', )


class SiteTypeAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
    ]

    list_display = [
        'id',
        'name',
        'created_on',
    ]

    list_display_links = [
        'id',
        'name',
    ]

    autocomplete_fields = [
        'metadata_schema'
    ]

    fieldsets = (
        (None, {
            'fields': (
                'name',
                'description'
            ),
        }),
        ('Schemas', {
            'fields': (
                ('metadata_schema'),
            )
        }),
    )

    inlines = [
        SiteDescriptorTypeInline
    ]
