from django.contrib import admin


class CollectionAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    search_fields = (
        'id',
        'name',
        'collection_type__name',
        'institution__institution_name',
    )
    list_display = (
        'id',
        'name',
        'collection_type',
        'institution',
    )
    list_filter = (
        'is_open',
        'collection_type',
        'institution',
    )
    autocomplete_fields = (
        'collection_type',
        'users',
        'administrators',
    )

    fieldsets = (
        (None, {
            'fields': (
                ('collection_type', 'name'),
                ('description',),
                ('institution', 'logo'),
            )
        }),
        ('Metadata', {
            'classes': ('collapse', ),
            'fields': ('metadata', )
        }),
        # ('Sites and Devices', {
            # 'classes': ('collapse', ),
            # 'fields': ('sites', 'physical_devices'),
        # }),
        ('Admin', {
            'classes': ('collapse', ),
            'fields': ('administrators', ),
        }),
        ('Access', {
            'classes': ('collapse', ),
            'fields': ('is_open', ),
        })
    )
