from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase
from irekua_database.models import Role
from irekua_collections.mixins import CollectionMetadataSchemaMixin


class CollectionTypeRole(IrekuaModelBase, CollectionMetadataSchemaMixin):
    collection_type = models.ForeignKey(
        "CollectionType",
        on_delete=models.CASCADE,
        db_column="collection_type_id",
        verbose_name=_("collection type"),
        help_text=_("Collection type in which role applies"),
        blank=False,
        null=False,
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        db_column="role_id",
        verbose_name=_("role"),
        help_text=_("Role to be part of collection"),
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = _("Collection Type Role")

        verbose_name_plural = _("Collection Type Roles")

        unique_together = (("collection_type", "role"),)

    def __str__(self):
        msg = _("Collection %(collection)s: Role %(role)s")
        params = dict(role=str(self.role), collection=str(self.collection_type))
        return msg % params
