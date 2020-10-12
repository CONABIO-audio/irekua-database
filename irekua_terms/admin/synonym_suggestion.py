from django.contrib import admin


class SynonymSuggestionAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'

    list_display = [
        'id',
        'synonym',
        'source',
    ]

    list_filter = [
        'source__term_type',
    ]

    list_display_links = [
        'id',
        'synonym',
    ]

    search_fields = [
        'synonym',
        'source__value',
        'source__term_type__name',
    ]

    autocomplete_fields = [
        'source',
    ]

    readonly_fields = [
        'created_on',
        'modified_on',
        'created_by',
        'modified_by',
    ]

    fieldsets = (
        (None, {
            'fields': (
                ('source', 'synonym'),
                'description',
            )
        }),
        ('Metadata', {
            'fields': ('metadata', ),
            'classes': ('collapse', )
        }),
        ('Creation', {
            'fields': (
                ('created_by', 'created_on'),
                ('modified_by', 'modified_on'),
            ),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)
