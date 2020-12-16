from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBaseUser
from irekua_items.models import Item


class ModelRun(IrekuaModelBaseUser):
    model_version = models.ForeignKey(
        "ModelVersion",
        on_delete=models.PROTECT,
        db_column="model_version_id",
        verbose_name=_("model version"),
        help_text=_("Model and version used for item processing"),
        blank=False,
        null=False,
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        db_column="item_id",
        verbose_name=_("item"),
        help_text=_("Item on which the model was run"),
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = _("Model Run")

        verbose_name_plural = _("Model Runs")

        ordering = ["-modified_on"]

    def __str__(self):
        msg = _("Model %(model_version)s run on item %(item)s)")
        params = dict(model_version=self.model_version, item=self.item)
        return msg % params

    def clean(self):
        super().clean()

        # Check that this model can process this item
        self.clean_item_type()

    def clean_item_type(self):
        # pylint: disable=no-member
        model = self.model_version.model
        item_type = self.item.item_type

        try:
            model.validate_item_type(item_type)

        except ValidationError as error:
            raise ValueError({"item": error}) from error
