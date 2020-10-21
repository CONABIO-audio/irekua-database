from django.contrib import admin


class OrganismCaptureAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    search_fields = ['organism__name']
    list_display = (
        'id',
        'collection',
        'sampling_event',
        'sampling_event_device',
        'organism',
        'organism_capture_type',
        'created_on',
        'created_by',
    )
    list_display_links = ('id',)
    readonly_fields = ('created_by', 'created_on')
    list_filter = (
        'created_on',
        'created_by',
        'organism_capture_type',
        'sampling_event_device',
        'organism')

    autocomplete_fields = (
        'labels',
        'sampling_event_device',
        'organism_capture_type',
        'organism')

    fieldsets = (
        (None, {
            'fields': (
                ('organism_capture_type',),
                ('organism', 'sampling_event_device'),
            )
        }),
        ('Additional metadata', {
            'classes': ('collapse',),
            'fields': ('additional_metadata',),
        }),
        ('Descriptors', {
            'classes': ('collapse',),
            'fields': ('labels',),
        }),
        ('Creation', {
            'classes': ('collapse',),
            'fields': (('created_by', 'created_on'),),
        })
    )

    def collection(self, obj):
        return obj.sampling_event_device.sampling_event.collection

    def sampling_event(self, obj):
        return obj.sampling_event_device.sampling_event

    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
