from django.contrib import admin


class OrganismTypeAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    search_fields = ['name']
    list_display = (
        'id',
        'name',
        'is_multi_organism',
    )
    list_display_links = ('id', 'name',)
    list_filter = ('is_multi_organism', 'created_on')

    autocomplete_fields = ('term_types',)
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'icon'),
                'description',
                'is_multi_organism',
            )
        }),
        ('Identification', {
            'classes': ('collapse',),
            'fields': ('identification_info_schema',),
        }),
        ('Descriptors', {
            'classes': ('collapse',),
            'fields': ('term_types',),
        })
    )
