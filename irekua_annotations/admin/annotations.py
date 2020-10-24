from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaUserAdmin
from irekua_items.models import Annotation
from irekua_items.models import AnnotationVote


class LabelsInline(admin.TabularInline):
    extra = 0

    model = Annotation.labels.through

    verbose_name = _('Label')

    verbose_name_plural = _('Labels')

    autocomplete_fields = [
        'term',
    ]



class AnnotationVoteInline(admin.TabularInline):
    extra = 0

    model = AnnotationVote

    fk_name = 'annotation'

    verbose_name = _('Annotation Vote')

    verbose_name_plural = _('Annotation Votes')

    autocomplete_fields = [
        'labels',
    ]

    readonly_fields = [
        'created_by',
        'created_on',
        'modified_by'
    ]


    fields = [
        'incorrect_geometry',
        'labels',
        'created_by',
        'created_on',
        'modified_by',
    ]


class AnnotationAdmin(IrekuaUserAdmin):
    search_fields = [
        'id',
        'item__id',
        'event_type__name',
        'annotation_type__name',
        'labels__value',
        'labels__term_type__name',
    ]

    list_display = [
        'id',
        'item',
        'event_type',
        'annotation_type',
        'created_by',
        'created_on',
    ]

    list_display_links = [
        'id',
    ]

    autocomplete_fields = [
        'item',
        'event_type',
        'annotation_type',
    ]

    fieldsets = (
        (None, {
            'fields': (
                'item',
                ('event_type','annotation_type'),
                'annotation',
            )
        }),
        (_('Additional Metadata'), {
            'fields': (
                ('annotation_metadata', 'event_metadata'),
            )
        }),
    )

    inlines = [
        LabelsInline,
        AnnotationVoteInline,
    ]

    def save_related(self, request, form, formsets, change):
        user = request.user
        vote_formset = formsets[1]
        for vote_form in vote_formset:
            if vote_form.instance.pk is None:
                vote_form.instance.created_by = user

            if vote_form.has_changed():
                vote_form.instance.modified_by = user

        return super().save_related(request, form, formsets, change)
