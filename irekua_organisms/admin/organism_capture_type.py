from django.contrib import admin


class OrganismCaptureTypeAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    search_fields = ['name']
    list_display = (
        'id',
        'name',
        'organism_type',
        'device_type'
    )

    autocomplete_fields = ('device_type', 'organism_type', 'term_types')

    fieldsets = (
        (None, {
            'fields': (
                ('name', 'icon'),
                'description',
                ('device_type', 'organism_type'),
            )
        }),
        ('Descriptors', {
            'classes': ('collapse',),
            'fields': ('term_types',),
        })
    )
