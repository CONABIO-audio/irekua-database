from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_terms.models import Entailment
from irekua_terms.models import Synonym


class SynonymInline(admin.TabularInline):
    extra = 0

    model = Synonym
    fk_name = 'source'

    autocomplete_fields = [
        'target',
    ]

    verbose_name = _('Synonym')
    verbose_name_plural = _('Synonyms')

    classes = ('collapse', )


class EntailmentInline(admin.TabularInline):
    extra = 0

    model = Entailment
    fk_name = 'source'

    autocomplete_fields = [
        'target',
    ]

    verbose_name = _('Entailment')
    verbose_name_plural = _('Entailments')

    classes = ('collapse', )


class TermAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'

    list_display = (
        'id',
        'value',
        'term_type',
    )

    list_filter = [
        'term_type',
    ]

    list_display_links = [
        'id',
        'value',
    ]

    search_fields = [
        'term_type__name',
        'value',
    ]

    autocomplete_fields = [
        'term_type',
    ]

    readonly_fields = [
        'created_on',
        'modified_on',
    ]

    fieldsets = (
        (None, {
            'fields': (
                ('term_type', 'value'),
                'description',
                ('scope', 'url'),
            )
        }),
        ('Metadata', {
            'fields': ('metadata', ),
            'classes': ('collapse', ),
        }),
        ('Creation', {
            'fields': (
                'created_on',
                'modified_on',
            ),
        })
    )

    inlines = [
        SynonymInline,
        EntailmentInline,
    ]
