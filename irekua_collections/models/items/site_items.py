import os

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_items.models import Item
from .collection_items import CollectionItemMixin


class SiteItemMixin(CollectionItemMixin):
    collection_site = models.ForeignKey(
        "CollectionSite",
        db_column="collection_site_id",
        verbose_name=_("collection site"),
        help_text=_("Site in which this item was captured"),
        on_delete=models.PROTECT,
        blank=False,
        null=False,
    )

    class Meta:
        abstract = True

    def clean(self):
        # Check that collection device belongs and
        # collection coincide
        self.clean_compatible_site_and_collection()

        super().clean()

    def clean_compatible_site_and_collection(self):
        if self.collection is None:
            # pylint: disable=no-member
            self.collection = self.collection_site.collection

        # pylint: disable=no-member
        if self.collection == self.collection_site.collection:
            return

        msg = _(
            "The site in which this item was captured (%(collection_site)s) does "
            "not belong to the collection %(collection)s."
        )
        params = dict(collection_site=self.collection_site, collection=self.collection)
        raise ValidationError({"collection_site": msg % params})


class SiteItem(Item, SiteItemMixin):
    upload_to_format = os.path.join(
        "items",
        "collection" "{collection}",
        "site" "{site}",
        "{hash}{ext}",
    )

    class Meta:
        verbose_name = _("Site Item")

        verbose_name_plural = _("Site Items")

        ordering = ["-created_on"]

    def clean_allowed_item_level(self, item_type_config):
        if not item_type_config.site_item:
            msg = _(
                "Item of type %(item_type)s are cannot be declared at the site "
                "level for collections of type %(collection_type)s"
            )
            params = dict(
                item_type=self.item_type,
                collection_type=item_type_config.collection_type,
            )
            raise ValidationError({"item_type": msg % params})

    def get_upload_to_format_arguments(self):
        return {
            **super().get_upload_to_format_arguments(),
            # pylint: disable=no-member
            "site": self.collection_site.id,
        }
