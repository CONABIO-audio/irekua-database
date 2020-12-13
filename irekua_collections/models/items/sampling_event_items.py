import os

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_items.models import Item
from .site_items import SiteItemMixin


class SamplingEventItemMixin(SiteItemMixin):
    sampling_event = models.ForeignKey(
        "SamplingEvent",
        db_column="sampling_event_id",
        verbose_name=_("sampling event"),
        help_text=_("Sampling event in which this item was captured"),
        on_delete=models.PROTECT,
        blank=False,
        null=False,
    )

    class Meta:
        abstract = True

    def clean(self):
        # Check that sampling event belongs to the declared collection
        self.clean_compatible_sampling_event_and_collection()

        #  Check that collection site coincides with the one declared by
        # the sampling event
        self.clean_compatible_sampling_event_and_site()

        super().clean()

        # Check if items of this type are allowed in sampling
        # events of this type.
        self.clean_compatible_item_type()

        # Check that captured on date is within the limits of the
        # sampling event
        self.clean_valid_captured_on()

    def clean_compatible_sampling_event_and_collection(self):
        if self.collection is None:
            # pylint: disable=no-member
            self.collection = self.sampling_event.collection

        # pylint: disable=no-member
        if self.collection == self.sampling_event.collection:
            return

        msg = _(
            "The sampling event in which the item was captured (%(sampling_event)s) "
            "does not belong to the collection %(collection)s."
        )
        params = dict(sampling_event=self.sampling_event, collection=self.collection)
        raise ValidationError({"sampling_event": msg % params})

    def clean_compatible_sampling_event_and_site(self):
        if self.collection_site is None:
            # pylint: disable=no-member
            self.collection_site = self.sampling_event.collection_site

        # pylint: disable=no-member
        if self.collection_site == self.sampling_event.collection_site:
            return

        msg = _(
            "The sampling event %(sampling_event)s occured on a different site than"
            "what was declared %(collection_site)s"
        )
        params = dict(
            sampling_event=self.sampling_event, collection_site=self.collection_site
        )
        raise ValidationError({"sampling_event": msg % params})

    def clean_compatible_item_type(self):
        # pylint: disable=no-member
        sampling_event_type = self.sampling_event.sampling_event_type

        try:
            sampling_event_type.validate_item_type(self.item_type)
        except ValidationError as error:
            raise ValidationError({"item_type": error}) from error

    def clean_valid_captured_on(self):
        if self.captured_on is None:
            return

        try:
            # pylint: disable=no-member
            self.sampling_event.validate_date(self.captured_on)

        except ValidationError as error:
            raise ValidationError({"captured_on": error}) from error


class SamplingEventItem(Item, SamplingEventItemMixin):
    upload_to_format = os.path.join(
        "items",
        "collection",
        "{collection}",
        "sampling_event",
        "{sampling_event}",
        "{hash}{ext}",
    )

    class Meta:
        verbose_name = _("Sampling Event Item")

        verbose_name_plural = _("Sampling Event Items")

        ordering = ["-created_on"]

    def clean_allowed_item_level(self, item_type_config):
        if not item_type_config.sampling_event_item:
            msg = _(
                "Item of type %(item_type)s are cannot be declared at the sampling "
                "event level for collections of type %(collection_type)s"
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
            "sampling_event": self.sampling_event.id,
        }
