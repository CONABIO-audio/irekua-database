from django.contrib import admin


class TermAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'term_type',
        'value',
    )
    search_fields = ['term_type__name', 'value']
    autocomplete_fields = ['term_type']
