from django.contrib import admin

from irekua_schemas import models

from .schemas import SchemaAdmin

admin.site.register(models.Schema, SchemaAdmin)
