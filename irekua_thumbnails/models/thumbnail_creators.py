import os
import importlib.util

from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase
from irekua_items.models import ItemType


class ThumbnailCreator(IrekuaModelBase):
    name = models.CharField(
        max_length=64,
        db_column="name",
        verbose_name=_("name"),
        unique=True,
        help_text=_("Name of thumbnail creator"),
        blank=False,
    )

    python_file = models.FileField(
        upload_to="thumbnail_creators/",
        db_column="python_file",
        verbose_name=_("python file"),
        help_text=_("Python file containing the thumbnail creator function"),
        blank=False,
        null=False,
    )

    item_types = models.ManyToManyField(
        ItemType,
        through="ThumbnailCreatorItemType",
        through_fields=("thumbnail_creator", "item_type"),
        verbose_name=_("item types"),
        help_text=_(
            "Item types that can be processed by this thumbnail creator"
        ),
    )

    class Meta:
        verbose_name = _("Thumbnail creator")

        verbose_name_plural = _("Thumbnail creators")

        ordering = ["-created_on"]

    def __str__(self):
        return self.name

    @staticmethod
    def load_creator_from_text(text):
        # pylint: disable=exec-used
        exec(text, locals())
        return locals()["thumbnail_creator"]

    def get_creator(self):
        with self.python_file.open() as py_file:
            text = py_file.read()

        return self.load_creator_from_text(text)

    @staticmethod
    def get_thumbnail_creator(item_type):
        Model = ThumbnailCreator.item_types.through
        return Model.objects.get(
            item_type=item_type, is_active=True
        ).thumbnail_creator
