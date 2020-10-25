from django.contrib import admin

from selia_annotator import models

from .annotators import AnnotatorAdmin
from .annotator_versions import AnnotatorVersionAdmin
from .annotation_annotators import AnnotationAnnotatorAdmin


admin.site.register(models.Annotator, AnnotatorAdmin)
admin.site.register(models.AnnotatorVersion, AnnotatorVersionAdmin)
admin.site.register(models.AnnotationAnnotator, AnnotationAnnotatorAdmin)
