from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaAdmin


class AnnotationAnnotatorAdmin(IrekuaAdmin):
    search_fields = [
        'annotation__id',
        'annotator_version__annotator__name',
    ]

    list_display = [
        'id',
        'annotation',
        'annotator_version',
        'created_on',
    ]

    list_display_links = [
        'id',
        'annotation',
    ]

    autocomplete_fields = [
        'annotation',
        'annotator_version',
    ]

    list_filter = [
        'annotation__annotation_type',
        'annotator_version__annotator__annotation_type',
    ]


    fieldsets = (
        (None, {
            'fields': (
                ('annotation', 'annotator_version'),
                'annotator_configuration'
            )
        }),
    )
