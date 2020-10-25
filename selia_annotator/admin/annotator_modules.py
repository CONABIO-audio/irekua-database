from django.contrib import admin


class AnnotatorModuleAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'

    search_fields = [
        'annotator__name',
        'version',
    ]

    list_display = [
        'id',
        'annotator',
        'version',
        'created_on',
    ]

    list_display_links = [
        'id',
        'version',
    ]

    autocomplete_fields = [
        'annotator',
    ]

    list_filter = [
        'annotator',
    ]

    readonly_fields = (
        'created_on',
        'modified_on',
    )

    fieldsets = (
        (None, {
            'fields': (
                ('annotator', 'version',),
                ('javascript_file', 'is_active'),
            )
        }),
        ('Creation', {
            'fields': (
                ('created_on', 'modified_on'),
            )
        }),
    )
