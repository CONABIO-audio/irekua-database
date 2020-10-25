from django.contrib import admin

from selia_visualizers import models
from .visualizer import VisualizerAdmin
from .visualizer_version import VisualizerVersionAdmin
from .annotation_visualizers import AnnotationVisualizerAdmin


admin.site.register(models.Visualizer, VisualizerAdmin)
admin.site.register(models.VisualizerVersion, VisualizerVersionAdmin)
admin.site.register(models.AnnotationVisualizer, AnnotationVisualizerAdmin)
