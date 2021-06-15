import os

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_items.models import Item


class CollectionItemsManager(models.Manager):
    def open(self):
        """Returns a query set with all items that are open access."""
        return self.filter(
            models.Q(licence__is_active=False)
            | models.Q(licence__licence_type__can_view=True)
        )

    def user(self, user):
        """Returns a queryset of all the collection items a user owns"""
        return self.filter(created_by=user)

    def managed(self, user):
        """Returns a queryset of all items that belong to a collection of a
        type managed by the user."""
        managed_collection_types = user.collectiontype_set.all()
        return self.filter(
            collection__collection_type__in=managed_collection_types
        )

    def administered(self, user):
        """Returns a queryset of all items that belong to a collection
        administered by the user."""
        administered_collections = user.collection_administrators.all()
        return self.filter(collection__in=administered_collections)

    def shared(self, user):
        """Returns a queryset of all items stored in collections to which the
        user has access."""
        collections_with_view_permission = user.collection_users.filter(
            collectionuser__role__permissions__codename="view_collectionitem"
        )
        return self.filter(collection__in=collections_with_view_permission)

    def can_view(self, user):
        if not user.is_authenticated:
            return self.open()

        if user.is_special:
            return self.all()

        return self.open().union(
            self.user(user),
            self.managed(user),
            self.administered(user),
            self.shared(user),
        )


class CollectionItem(Item):
    COLLECTION = "collection"
    SITE = "site"
    DEPLOYMENT = "deployment"
    DEVICE = "device"
    SAMPLING_EVENT = "sampling event"
    LEVELS = [
        COLLECTION,
        SITE,
        DEPLOYMENT,
        DEVICE,
        SAMPLING_EVENT,
    ]

    objects = CollectionItemsManager()

    upload_to_format = os.path.join(
        "items",
        "collection",
        "{collection}",
        "{hash}{ext}",
    )

    collection = models.ForeignKey(
        "irekua_collections.Collection",
        db_column="collection_id",
        verbose_name=_("collection"),
        help_text=_("Collection to which this item belongs"),
        on_delete=models.PROTECT,
        blank=True,
        null=False,
    )

    collection_metadata = models.JSONField(
        db_column="collection_metadata",
        verbose_name=_("collection metadata"),
        help_text=_("Additional metadata associated to item in collection"),
        blank=True,
        null=True,
    )

    collection_device = models.ForeignKey(
        "irekua_collections.CollectionDevice",
        db_column="collection_device_id",
        verbose_name=_("collection device"),
        help_text=_("Device used to capture the item"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    collection_site = models.ForeignKey(
        "irekua_collections.CollectionSite",
        db_column="collection_site_id",
        verbose_name=_("collection site"),
        help_text=_("Site in which this item was captured"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    sampling_event = models.ForeignKey(
        "irekua_collections.SamplingEvent",
        db_column="sampling_event_id",
        verbose_name=_("sampling event"),
        help_text=_("Sampling event in which this item was captured"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    deployment = models.ForeignKey(
        "irekua_collections.Deployment",
        db_column="deployment_id",
        verbose_name=_("deployment"),
        help_text=_("Deployment of device in which this item was captured"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Collection Item")

        verbose_name_plural = _("Collection Items")

    def clean(self):
        super().clean()

        if self.collection_site is not None:
            self.clean_item_site()

        if self.collection_device is not None:
            return self.clean_item_device()

        if self.sampling_event is not None:
            return self.clean_item_sampling_event()

        if self.deployment is not None:
            return self.clean_item_deployment()

        self.clean_collection_item()

    def clean_collection_item(self):
        try:
            # pylint: disable=no-member
            collection_type = self.collection.collection_type
        except (ObjectDoesNotExist, AttributeError):
            msg = _("A collection must be provided")
            raise ValidationError({"collection": msg})

        # If collection type does not restrict item types no further
        # validation is required
        if not collection_type.restrict_item_types:
            return

        # Check if this item type is permitted in this collection type
        item_type_config = self.clean_allowed_item_type(collection_type)

        # Check if this type of items can be associated at the correct
        # level
        self.clean_allowed_item_level(item_type_config)

        # Check if collection metadata is valid for this item type
        self.clean_valid_collection_metadata(item_type_config)

    def clean_item_site(self):
        # Check that the declared site belongs to the declared collection.
        self.clean_site_collection()

    def clean_item_device(self):
        # Check that the declared device belongs to the declared collection.
        self.clean_device_collection()

        # Check that the device can produce items of the declared type
        self.clean_compatible_device_and_item_type()

    def clean_item_sampling_event(self):
        # Check that the declared site coincided with the sampling event site
        self.clean_sampling_event_site()

        if self.deployment is not None:
            # Avoid more validation if item was declared at deployment level
            return

        # Check if items of this type are allowed in sampling
        # events of this type.
        self.clean_compatible_sampling_event_and_item_type()

        # Check that captured on date is within the limits of the
        # sampling event
        self.clean_valid_captured_on_sampling_event()

    def clean_item_deployment(self):
        # Check that the declared deployed occurred in the declared
        # sampling event
        self.clean_deployment_sampling_event()

        # Check that the declared deployed device coincides with the
        # declared device.
        self.clean_deployment_device()

        # Check if items of this type are allowed in sampling
        # events of this type.
        self.clean_compatible_deployment_and_item_type()

        # Check that captured on date is within the limits of the
        # sampling event
        self.clean_valid_captured_on_deployment()

    def clean_sampling_event_site(self):
        if self.collection_site is None:
            # pylint: disable=no-member
            self.collection_site = self.sampling_event.collection_site
            self.clean_site_collection()

        # pylint: disable=no-member
        if self.collection_site == self.sampling_event.collection_site:
            return

        msg = _(
            "The sampling event in which this item was captured "
            "(%(sampling_event)s) was conducted in a different site "
            "to the one declared (%(collection_site)s)"
        )
        params = dict(
            collection_site=self.collection_site,
            sampling_event=self.sampling_event,
        )
        raise ValidationError({"collection_site": msg % params})

    def clean_deployment_sampling_event(self):
        if self.sampling_event is None:
            self.sampling_event = self.deployment.sampling_event
            self.clean_sampling_event_site()

        # pylint: disable=no-member
        if self.sampling_event == self.deployment.sampling_event:
            return

        msg = _(
            "The deployment in which the item was captured (%(deployment)s) "
            "does not belong to the sampling event %(sampling_event)s."
        )
        params = dict(
            deployment=self.deployment,
            sampling_event=self.sampling_event,
        )
        raise ValidationError({"deployment": msg % params})

    def clean_deployment_device(self):
        if self.collection_device is None:
            # pylint: disable=no-member
            self.collection_device = self.deployment.collection_device
            self.clean_device_collection()

        # pylint: disable=no-member
        if self.collection_device == self.deployment.collection_device:
            return

        msg = _(
            "The device that captured the item (%(collection_device)s) "
            "does not coincide with the deployed device %(deployment)s."
        )
        params = dict(
            collection_device=self.collection_device,
            deployment=self.deployment,
        )
        raise ValidationError({"deployment": msg % params})

    def clean_site_collection(self):
        if self.collection is None:
            self.collection = self.collection_site.collection

        if self.collection == self.collection_site.collection:
            return

        msg = _(
            "The site in which this item was captured (%(collection_site)s) "
            "does not belong to the collection %(collection)s."
        )
        params = dict(
            collection_site=self.collection_site,
            collection=self.collection,
        )
        raise ValidationError({"collection_site": msg % params})

    def clean_device_collection(self):
        if self.collection is None:
            # pylint: disable=no-member
            self.collection = self.collection_device.collection

        # pylint: disable=no-member
        if self.collection == self.collection_device.collection:
            return

        msg = _(
            "The device with which this item was captured "
            "(%(collection_device)s) does not belong to the "
            "collection %(collection)s."
        )
        params = dict(
            collection_device=self.collection_device,
            collection=self.collection,
        )
        raise ValidationError({"collection_device": msg % params})

    def clean_compatible_device_and_item_type(self):
        # pylint: disable=no-member
        device_type = self.collection_device.physical_device.device.device_type

        try:
            device_type.validate_mime_type(self.mime_type)

        except ValidationError as error:
            raise ValidationError({"mime_type": error}) from error

    def clean_compatible_deployment_and_item_type(self):
        # pylint: disable=no-member
        deployment_type = self.deployment.deployment_type

        try:
            deployment_type.validate_item_type(self.item_type)

        except ValidationError as error:
            raise ValidationError({"item_type": error}) from error

    def clean_allowed_item_type(self, collection_type):
        try:
            return collection_type.get_item_type(self.item_type)

        except ObjectDoesNotExist as error:
            msg = _(
                "Item of type %(item_type)s are not allowed in "
                "collections of type %(collection_type)s"
            )
            params = dict(
                item_type=self.item_type,
                collection_type=collection_type,
            )
            raise ValidationError({"item_type": msg % params}) from error

    def clean_allowed_item_level(self, item_type_config):
        level = self.get_item_level()

        if (level is self.COLLECTION) and item_type_config.collection_item:
            return

        if (level is self.DEVICE) and item_type_config.device_item:
            return

        if (level is self.SITE) and item_type_config.site_item:
            return

        if (
            level is self.SAMPLING_EVENT
            and item_type_config.sampling_event_item
        ):
            return

        if (level is self.DEPLOYMENT) and item_type_config.deployment_item:
            return

        if not item_type_config.collection_item:
            msg = _(
                "Item of type %(item_type)s are cannot be declared at a "
                "%(level)s level for collections of type "
                "%(collection_type)s"
            )
            params = dict(
                item_type=self.item_type,
                level=level,
                collection_type=item_type_config.collection_type,
            )
            raise ValidationError({"item_type": msg % params})

    def clean_valid_captured_on_sampling_event(self):
        if self.captured_on is None:
            return

        try:
            # pylint: disable=no-member
            self.sampling_event.validate_date(self.captured_on)

        except ValidationError as error:
            raise ValidationError({"captured_on": error}) from error

    def clean_valid_captured_on_deployment(self):
        if self.captured_on is None:
            return

        try:
            # pylint: disable=no-member
            self.deployment.validate_date(self.captured_on)

        except ValidationError as error:
            raise ValidationError({"captured_on": error}) from error

    def clean_valid_collection_metadata(self, item_type_config):
        try:
            item_type_config.validate_metadata(self.collection_metadata)

        except ValidationError as error:
            raise ValidationError(
                {"collection_metadata": str(error)}
            ) from error

    def clean_compatible_sampling_event_and_item_type(self):
        # pylint: disable=no-member
        sampling_event_type = self.sampling_event.sampling_event_type

        try:
            sampling_event_type.validate_item_type(self.item_type)

        except ValidationError as error:
            raise ValidationError({"item_type": error}) from error

    def get_item_level(self):
        if self.deployment is not None:
            return self.DEPLOYMENT

        if self.sampling_event is not None:
            return self.SAMPLING_EVENT

        if self.collection_device is not None:
            return self.DEVICE

        if self.collection_site is not None:
            return self.SITE

        return self.COLLECTION

    def get_upload_to_format_arguments(self):
        return {
            **super().get_upload_to_format_arguments(),
            # pylint: disable=no-member
            "collection": self.collection.id,
        }

    from irekua_collections.permissions.collection_items import can_view
    from irekua_collections.permissions.collection_items import can_change
    from irekua_collections.permissions.collection_items import can_delete
