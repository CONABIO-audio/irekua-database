from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_database.models import SamplingEventType


class SiteTypeInline(admin.TabularInline):
    extra = 0
    model = SamplingEventType.site_types.through
    autocomplete_fields = ('sitetype',)
    verbose_name = _('Site type')
    verbose_name_plural = _('Site types')
    classes = ('collapse', )


class DeploymentTypeInline(admin.TabularInline):
    extra = 0
    model = SamplingEventType.deployment_types.through
    autocomplete_fields = ('deploymenttype',)
    verbose_name = _('Deployment type')
    verbose_name_plural = _('Deployment types')
    classes = ('collapse', )


class SamplingEventTypeAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    search_fields = ('name', )
    list_display = (
        'id',
        'name',
        'restrict_site_types',
        'restrict_deployment_types',
        'created_on')
    list_display_links = ('id', 'name')
    list_filter = ('created_on', 'restrict_site_types', 'restrict_deployment_types')

    fieldsets = (
        (None, {
            'fields': (
                ('name', 'icon'),
                'description'
            ),
        }),
        ('Metadata', {
            'classes': ('collapse', ),
            'fields': ('metadata_schema', ),
        }),
        ('Restrictions', {
            'classes': ('collapse', ),
            'fields': (
                (
                    'restrict_site_types',
                    'restrict_deployment_types',
                ),
            ),
        }),
    )

    inlines = [
        SiteTypeInline,
        DeploymentTypeInline,
    ]
