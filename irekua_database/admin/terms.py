from django.contrib import admin


class TermAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'term_type',
        'value',
    )
    search_fields = ['term_type__name', 'value']
    autocomplete_fields = ['term_type']


class EntailmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'get_source_type',
        'source',
        'get_target_type',
        'target',
    )
    search_fields = [
        'source__value',
        'target__value',
    ]
    autocomplete_fields = ['source', 'target']

    def get_source_type(self, obj):
        return obj.source.term_type
    get_source_type.short_description = 'Source Type'
    get_source_type.admin_order_field = 'source__term_type__name'

    def get_target_type(self, obj):
        return obj.target.term_type
    get_target_type.short_description = 'Target Type'
    get_target_type.admin_order_field = 'target__term_type__name'


    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('source', 'target')

class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']
