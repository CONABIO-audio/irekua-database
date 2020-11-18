from django.contrib import admin
from django.contrib.auth.models import Permission

from irekua_database import models

from .users import UserAdmin
from .roles import RoleAdmin
from .institutions import InstitutionAdmin


admin.site.register(Permission)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Role, RoleAdmin)
admin.site.register(models.Institution, InstitutionAdmin)
