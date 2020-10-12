from django.contrib import admin


class EntailmentTypeAdmin(admin.ModelAdmin):
    search_fields = [
        'source_type__name',
        'target_type__name',
    ]

    list_display = (
        'id',
        'source_type',
        'target_type',
        'created_on',
    )

    list_display_links = (
        'id',
    )

    autocomplete_fields = [
        'source_type',
        'target_type',
    ]

    fields = (
        ('source_type', 'target_type'),
        'metadata_schema',
    )
