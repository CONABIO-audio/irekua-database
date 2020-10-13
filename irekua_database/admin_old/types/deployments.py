from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class DeploymentTypeAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'

    search_fields = (
        'name',
        'device_type__name',
    )

    list_display = (
        'id',
        'name',
        'device_type',
        'created_on'
    )

    list_display_links = (
        'id',
        'name'
    )

    list_filter = (
        'device_type',
    )

    readonly_fields = (
        'created_on',
        'modified_on',
    )

    fieldsets = (
        (None, {
            'fields': (
                ('name', 'icon'),
                'description',
                'device_type',
            ),
        }),
        ('Metadata', {
            'classes': ('collapse', ),
            'fields': ('metadata_schema', ),
        }),
        ('Creation', {
            'fields': (
                (
                    'created_on',
                    'modified_on',
                ),
            ),
        }),
    )
