from django.contrib import admin


class SynonymAdmin(admin.ModelAdmin):
    search_fields = [
        'source__value',
        'target__value',
    ]

    list_display = [
        'id',
        'source',
        'target',
    ]

    list_filter = [
        'source__term_type',
    ]

    autocomplete_fields = [
        'source',
        'target',
    ]

    fields = (
        ('source', 'target'),
        'metadata',
    )
