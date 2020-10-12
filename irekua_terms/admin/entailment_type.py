from django.contrib import admin


class EntailmentTypeAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('id', 'name', 'source_type', 'target_type', 'created_on')
    list_display_links = ('id', 'name')

    def name(self, obj):
        return str(obj)
