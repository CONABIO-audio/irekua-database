from django.contrib import admin


class CustomModelAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'

    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.created_by:
            instance.created_by = user
        instance.modified_by = user
        instance.save()
        form.save_m2m()
        return instance


class ModelAdmin(CustomModelAdmin):
    search_fields = ['name']
    list_display = (
        'id',
        'name',
        'annotation_type',
    )
    fields = (
        ('name', 'repository'),
        'description',
        ('annotation_type', 'item_types'),
        ('terms', 'event_types'),
    )
    autocomplete_fields = [
        'terms',
        'annotation_type',
        'event_types',
        'item_types']


class ModelVersionAdmin(CustomModelAdmin):
    search_fields = ['model__name']
    list_display_links = ('version', )
    list_filter = ('created_on', 'created_by')
    list_display = (
        'id',
        'model',
        'version',
        'created_on'
    )
    fields = (
        ('model', 'version'),)
    autocomplete_fields = ['model']


class ModelPredictionAdmin(CustomModelAdmin):
    list_display = (
        'id',
        'item',
        'model_version',
        'event_type',
        'certainty',
        'created_on',
        'created_by',
    )
    fields = (
        ('item', 'model_version', 'event_type'),
        'annotation',
        ('certainty', 'labels'))
    autocomplete_fields = [
        'item',
        'labels',
        'model_version',
        'event_type']
