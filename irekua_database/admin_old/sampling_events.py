from django.contrib import admin


class SamplingEventAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    search_fields = [
        'id',
        'collection_site__internal_id',
        'started_on']
    list_display = (
        'id',
        'collection_site',
        'started_on',
        'ended_on',
        'created_on')


class SamplingEventDeviceAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    search_fields = ['id']
