
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBaseUser


class PhysicalDevice(IrekuaModelBaseUser):
    name = models.CharField(
        max_length=128,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Device name (visible only to owner)'),
        blank=True)

    serial_number = models.CharField(
        max_length=128,
        db_column='serial_number',
        verbose_name=_('serial number'),
        help_text=_('Serial number of device'),
        blank=True,
        null=True)

    device = models.ForeignKey(
        'Device',
        on_delete=models.PROTECT,
        db_column='device_id',
        verbose_name=_('device'),
        help_text=_('Brand and model of device'),
        blank=False,
        null=False)

    metadata = models.JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to device'),
        null=True,
        blank=True)

    class Meta:
        verbose_name = _('Physical Device')

        verbose_name_plural = _('Physical Devices')

        unique_together = (
            ('serial_number', 'device'),
        )

        ordering = ['-created_on']

    def __str__(self):
        if self.name:
            return self.name

        msg = _('Device %(id)s of type %(device)s')
        params = dict(
            id=self.id,
            device=str(self.device))
        return msg % params

    def clean(self):
        super().clean()

        # Check metadata is valid for this device type
        self.clean_metadata()

    def clean_metadata(self):
        try:
            # pylint: disable=no-member
            self.device.validate_metadata(self.metadata)

        except ValidationError as error:
            raise ValidationError({'metadata': error}) from error

    @cached_property
    def items(self):
        from irekua_collections.models import DeploymentItem
        return DeploymentItem.objects.filter(
            deployment__collection_device__physical_device=self)

    @cached_property
    def sampling_events(self):
        from irekua_collections.models import SamplingEvent
        return SamplingEvent.objects.filter(
            collection_device__physical_device=self)

    @cached_property
    def deployments(self):
        from irekua_collections.models import Deployment
        return Deployment.objects.filter(
            sampling_event__collection_device__physical_device=self)
