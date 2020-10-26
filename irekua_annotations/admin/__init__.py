from django.contrib import admin

from irekua_annotations import models

from .annotations import AnnotationAdmin
from .annotation_votes import AnnotationVoteAdmin
from .annotation_types import AnnotationTypeAdmin
from .event_types import EventTypeAdmin
from .user_annotations import UserAnnotationAdmin


admin.site.register(models.Annotation, AnnotationAdmin)
admin.site.register(models.UserAnnotation, UserAnnotationAdmin)
admin.site.register(models.AnnotationVote, AnnotationVoteAdmin)
admin.site.register(models.AnnotationType, AnnotationTypeAdmin)
admin.site.register(models.EventType, EventTypeAdmin)
