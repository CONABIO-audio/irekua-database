from django.utils.translation import gettext_lazy as _
from .annotations import AnnotationAdmin


class UserAnnotationAdmin(AnnotationAdmin):
    list_display = [
        'id',
        'item',
        'event_type',
        'annotation_type',
        'certainty',
        'quality',
        'created_by',
        'created_on',
    ]

    fieldsets = (
        (None, {
            'fields': (
                'item',
                ('event_type','annotation_type'),
                'annotation',
            )
        }),
        (_('User commentaries'), {
            'fields': (
                ('certainty', 'quality'),
                'commentaries',
            ),
        }),
        (_('Additional Metadata'), {
            'fields': (
                ('annotation_metadata', 'event_metadata'),
            )
        }),
    )
