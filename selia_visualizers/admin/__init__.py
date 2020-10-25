from django.contrib import admin

from selia_visualizers import models
from selia_visualizers.admin.visualizer import VisualizerAdmin
from selia_visualizers.admin.visualizer_version import VisualizerVersionAdmin
from selia_visualizers.admin.visualizer_modules import VisualizerModuleAdmin


admin.site.register(models.Visualizer, VisualizerAdmin)
admin.site.register(models.VisualizerVersion, VisualizerVersionAdmin)
admin.site.register(models.VisualizerModule, VisualizerModuleAdmin)
