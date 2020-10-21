from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaAdmin
from irekua_collections.models import CollectionType


def sort_fields(fields):
    extra_fields = []
    for field in fields:
        if 'collection_type' in field or 'collectiontype' in field:
            collection_field = field

        elif 'role' in field or 'type' in field:
            type_field = field

        elif 'metadata' in field:
            metadata_field = field

        else:
            extra_fields.append(field)

    return [collection_field, type_field, metadata_field, *extra_fields]


def inline_factory(m2m_field):
    name = m2m_field.replace('_', ' ').title()

    class M2MInline(admin.TabularInline):
        extra = 0
        classes = ('collapse',)
        model = getattr(CollectionType, m2m_field).through
        verbose_name = _(name.rstrip('s'))
        verbose_name_plural = _(name)
        autocomplete_fields = [m2m_field.rstrip('s')]

        def get_fields(self, request, obj=None):
            return sort_fields(super().get_fields(request, obj=obj))

    return M2MInline


class AdministratorsInline(admin.TabularInline):
    extra = 0
    model = CollectionType.administrators.through
    verbose_name = _('Administrator')
    verbose_name_plural = _('Administrators')
    autocomplete_fields = ['user']


class CollectionTypeAdmin(IrekuaAdmin):
    search_fields = [
        'name',
    ]

    list_display = [
        'id',
        '__str__',
        'anyone_can_create',
        'restrict_item_types',
        'restrict_event_types',
        'restrict_sampling_event_types',
        'restrict_deployment_types',
        'restrict_annotation_types',
        'created_on',
    ]

    list_display_links = [
        'id',
        '__str__',
    ]

    fieldsets = (
        (None, {
            'fields': (
                ('name', 'logo'),
                'description',
                'anyone_can_create'
            )
        }),
        (_('Restrictions'), {
            'fields': (
                (
                    'restrict_site_types',
                    'restrict_annotation_types',
                    'restrict_item_types',
                    'restrict_licence_types',
                ),
                (
                    'restrict_device_types',
                    'restrict_event_types',
                    'restrict_sampling_event_types',
                    'restrict_deployment_types',
                ),
            ),
        })
    )

    inlines = [
        AdministratorsInline,
        inline_factory('roles'),
        inline_factory('site_types'),
        inline_factory('annotation_types'),
        inline_factory('item_types'),
        inline_factory('licence_types'),
        inline_factory('device_types'),
        inline_factory('event_types'),
        inline_factory('sampling_event_types'),
        inline_factory('deployment_types'),
    ]
