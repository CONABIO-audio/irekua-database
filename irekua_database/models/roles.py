from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase


class Role(IrekuaModelBase):
    name = models.CharField(
        max_length=64,
        unique=True,
        db_column="name",
        verbose_name=_("name"),
        help_text=_("Name of role"),
        blank=False,
        null=False,
    )

    description = models.TextField(
        db_column="description",
        verbose_name=_("description"),
        help_text=_("Description of role"),
        blank=True,
    )

    icon = models.ImageField(
        db_column="icon",
        verbose_name=_("icon"),
        help_text=_("Role type icon"),
        upload_to="images/role_types/",
        blank=True,
        null=True,
    )

    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("permissions"),
        help_text=_("Permissions associated to role"),
        blank=True,
    )

    class Meta:
        verbose_name = _("Role")

        verbose_name_plural = _("Roles")

        ordering = ["name"]

    def __str__(self):
        return str(self.name)

    def add_permission_from_codename(self, codename):
        if not isinstance(codename, (tuple, list)):
            codename = [codename]

        for code in codename:
            try:
                permission = Permission.objects.get(codename=code)
                self.permissions.add(permission)

            except ObjectDoesNotExist:
                pass

    def has_permission(self, codename):
        return self.permissions.filter(codename=codename).exists()
