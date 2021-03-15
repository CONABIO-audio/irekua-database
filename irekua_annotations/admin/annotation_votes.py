from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaUserAdmin
from irekua_annotations.models import AnnotationVote


class LabelsInline(admin.TabularInline):
    extra = 0

    model = AnnotationVote.labels.through

    verbose_name = _("Label")

    verbose_name_plural = _("Labels")

    autocomplete_fields = [
        "term",
    ]


class AnnotationVoteAdmin(IrekuaUserAdmin):
    search_fields = [
        "id",
        "annotation__id",
        "annotation__annotation_type__name",
        "annotation__event_type__name",
        "labels__value",
        "labels__term_type__name",
    ]

    list_display = [
        "id",
        "annotation",
        "incorrect_geometry",
        "created_by",
        "created_on",
    ]

    list_display_links = [
        "id",
    ]

    autocomplete_fields = [
        "annotation",
    ]

    fieldsets = ((None, {"fields": (("annotation", "incorrect_geometry"),)}),)

    inlines = [
        LabelsInline,
    ]
