from django.contrib import admin

from irekua_upload import models

from .operations import OperationAdmin


admin.site.register(models.Operation, OperationAdmin)
