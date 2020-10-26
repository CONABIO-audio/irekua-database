from django.utils.translation import gettext_lazy as _

from irekua_annotations.admin.user_annotations import UserAnnotationAdmin


class CollectionAnnotationAdmin(UserAnnotationAdmin):
    search_fields = [
        'collection__name',
        *UserAnnotationAdmin.search_fields,
    ]

    list_display = [
        'id',
        '__str__',
        'collection',
        'item',
        'event_type',
        'annotation_type',
        'certainty',
        'quality',
        'created_by',
        'created_on',
    ]

    list_filter = [
        'collection__collection_type',
        *UserAnnotationAdmin.list_filter,
    ]

    autocomplete_fields = [
        'collection',
        *UserAnnotationAdmin.autocomplete_fields,
    ]

    fieldsets = (
        (None, {
            'fields': (
                ('collection', 'item'),
                ('event_type','annotation_type'),
                'annotation',
            )
        }),
        (_('User Commentaries'), {
            'fields': (
                ('certainty', 'quality'),
                'commentaries',
            )
        }),
        (_('Additional Metadata'), {
            'fields': (
                ('annotation_metadata', 'event_metadata'),
                'collection_metadata'
            )
        }),
    )
