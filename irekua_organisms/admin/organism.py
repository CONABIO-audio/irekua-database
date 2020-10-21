from django.contrib import admin


class OrganismAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    search_fields = ['name', 'organism_type__name']
    list_display = (
        'id',
        'collection',
        'organism_type',
        'name',
        'created_by',
        'created_on',
    )
    readonly_fields = ('created_by', 'created_on')
    list_display_links = ('id', 'name',)
    list_filter = (
        'collection',
        'organism_type',
        'created_on',
        'created_by')

    autocomplete_fields = ('labels', 'collection', 'organism_type')
    fieldsets = (
        (None, {
            'fields': (
                ('collection', 'organism_type', 'name'),
                ('remarks',),
            )
        }),
        ('Identification', {
            'classes': ('collapse',),
            'fields': ('labels', 'identification_info'),
        }),
        ('Additional Metadata', {
            'classes': ('collapse',),
            'fields': ('additional_metadata',),
        }),
        ('Creation', {
            'classes': ('collapse',),
            'fields': (('created_by', 'created_on'),),
        })
    )

    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
