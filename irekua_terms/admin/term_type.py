from django.contrib import admin


class TermTypeAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('id', 'name', 'is_categorical', 'created_on')
    list_display_links = ('id', 'name')

    fieldsets = (
        (None, {
            'fields': (
                ('name', 'icon'),
                'description',
                'is_categorical',
            ),
        }),
        ('Additional metadata', {
            'classes': ('collapse', ),
            'fields': ('metadata_schema', 'synonym_metadata_schema')
        }),
    )
