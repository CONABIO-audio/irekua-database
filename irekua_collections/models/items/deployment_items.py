import os

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_items.models import Item
from .sampling_event_items import SamplingEventItemMixin
from .device_items import DeviceItemMixin


class DeploymentItemMixin(SamplingEventItemMixin, DeviceItemMixin):
    class Meta:
        abstract = True

    def clean(self):
        #  Check that the samplign event coincides with the one declared by
        # the deployment
        self.clean_compatible_deployment_and_sampling_event()

        # Check that the device used coincides with the one delared by the
        # deployment
        self.clean_compatible_deployment_and_device()

        super().clean()

    def clean_compatible_deployment_and_sampling_event(self):
        if self.sampling_event is None:
            # pylint: disable=no-member
            self.sampling_event = self.deployment.sampling_event

        # pylint: disable=no-member
        if self.sampling_event == self.deployment.sampling_event:
            return

        msg = _(
            "The deployment in which the item was captured (%(deployment)s) "
            "does not belong to the sampling event %(sampling_event)s."
        )
        params = dict(deployment=self.deployment, sampling_event=self.sampling_event)
        raise ValidationError({"deployment": msg % params})

    def clean_compatible_deployment_and_device(self):
        if self.collection_device is None:
            # pylint: disable=no-member
            self.collection_device = self.deployment.collection_device

        # pylint: disable=no-member
        if self.collection_device == self.deployment.collection_device:
            return

        msg = _(
            "The device that captured the item (%(collection_device)s) "
            "does not coincide with the deployed device %(deployment)s."
        )
        params = dict(
            collection_device=self.collection_device, deployment=self.deployment
        )
        raise ValidationError({"deployment": msg % params})

    def clean_compatible_item_type(self):
        # pylint: disable=no-member
        deployment_type = self.deployment.deployment_type

        try:
            deployment_type.validate_item_type(self.item_type)
        except ValidationError as error:
            raise ValidationError({"item_type": error}) from error

    def clean_valid_captured_on(self):
        if self.captured_on is None:
            return

        try:
            # pylint: disable=no-member
            self.deployment.validate_date(self.captured_on)

        except ValidationError as error:
            raise ValidationError({"captured_on": error}) from error

    def get_upload_to_format_arguments(self):
        return {
            **super().get_upload_to_format_arguments(),
            # pylint: disable=no-member
            "deployment": self.deployment.id,
        }


class DeploymentItemTmp(Item, DeploymentItemMixin):
    upload_to_format = os.path.join(
        "items",
        "collection",
        "{collection}",
        "sampling_event",
        "{sampling_event}",
        "deployment",
        "{deployment}",
        "{hash}{ext}",
    )

    class Meta:
        verbose_name = _("Deployment Item")

        verbose_name_plural = _("Deployment Items")

        ordering = ["-created_on"]

    def clean_allowed_item_level(self, item_type_config):
        if not item_type_config.deployment_item:
            msg = _(
                "Item of type %(item_type)s are cannot be declared at a deployment "
                "level for collections of type %(collection_type)s"
            )
            params = dict(
                item_type=self.item_type,
                collection_type=item_type_config.collection_type,
            )
            raise ValidationError({"item_type": msg % params})
