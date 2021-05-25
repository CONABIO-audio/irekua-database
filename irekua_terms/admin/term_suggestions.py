from django.contrib import admin


class TermSuggestionAdmin(admin.ModelAdmin):
    date_hierarchy = "created_on"

    list_display = [
        "id",
        "value",
        "term_type",
    ]

    list_filter = [
        "term_type",
    ]

    list_display_links = [
        "id",
        "value",
    ]

    search_fields = [
        "value",
        "term_type__name",
    ]

    autocomplete_fields = [
        "term_type",
    ]

    readonly_fields = [
        "created_on",
        "modified_on",
        "created_by",
        "modified_by",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("term_type", "value"),
                    "description",
                )
            },
        ),
        ("Metadata", {"fields": ("metadata",), "classes": ("collapse",)}),
        (
            "Creation",
            {
                "fields": (
                    ("created_by", "created_on"),
                    ("modified_by", "modified_on"),
                ),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)
