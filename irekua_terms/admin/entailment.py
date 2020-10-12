from django.contrib import admin


class EntailmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'source',
        'target',
    )

    search_fields = [
        'source__value',
        'target__value',
    ]

    autocomplete_fields = [
        'source',
        'target'
    ]

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            .prefetch_related(
                'source',
                'target',
                'source__term_type',
                'target__term_type',
            )
            .only(
                'id',
                'source',
                'target',
                'source__value',
                'target__value',
                'source__term_type',
                'target__term_type',
                'source__term_type__name',
                'target__term_type__name',
            )
        )
