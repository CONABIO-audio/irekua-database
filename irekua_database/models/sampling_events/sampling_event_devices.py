from django.contrib.postgres.fields import JSONField
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.utils import empty_JSON
from irekua_database.models.base import IrekuaModelBaseUser


class SamplingEventDevice(IrekuaModelBaseUser):
    sampling_event = models.ForeignKey(
        'SamplingEvent',
        on_delete=models.PROTECT,
        db_column='sampling_event_id',
        verbose_name=_('sampling event'),
        help_text=_('Sampling event in which this device was deployed'),
        blank=False,
        null=False)

    deployed_on = models.DateTimeField(
        db_column='deployed_on',
        verbose_name=_('deployed on'),
        help_text=_('Date at which the device started capturing information.'),
        blank=True,
        null=True)
    recovered_on = models.DateTimeField(
        db_column='recovered_on',
        verbose_name=_('recovered on'),
        help_text=_('Date at which the device stoped capturing information.'),
        blank=True,
        null=True)
    collection_device = models.ForeignKey(
        'CollectionDevice',
        db_column='collection_device_id',
        verbose_name=_('collection device'),
        help_text=_('Reference to collection device used on sampling event'),
        on_delete=models.PROTECT,
        blank=True,
        null=True)
    commentaries = models.TextField(
        db_column='commentaries',
        verbose_name=_('commentaries'),
        help_text=_('Sampling event commentaries'),
        blank=True)
    metadata = JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to sampling event device'),
        default=empty_JSON,
        blank=True,
        null=True)
    configuration = JSONField(
        db_column='configuration',
        verbose_name=_('configuration'),
        default=empty_JSON,
        help_text=_('Configuration on device through the sampling event'),
        blank=True,
        null=True)
    licence = models.ForeignKey(
        'Licence',
        on_delete=models.PROTECT,
        db_column='licence_id',
        verbose_name=_('licence'),
        help_text=_('Licence for all items in sampling event'),
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Sampling Event Device')
        verbose_name_plural = _('Sampling Event Devices')

        unique_together = (
            ('sampling_event', 'collection_device'),
        )

        ordering = ['-created_on']

    def __str__(self):
        msg = _('Deployed Device {id}')
        msg = msg.format(id=str(self.id))
        return msg

    def validate_licence(self):
        if self.licence is not None:
            self.licence = self.sampling_event.licence

        if self.licence is not None:
            collection = self.sampling_event.collection
            collection.validate_and_get_licence(self.licence)

    def validate_user(self):
        if self.created_by is None:
            self.created_by = self.sampling_event.created_by

        if self.created_by is None:
            return

    def validate_deployed_on(self):
        starting_date = self.sampling_event.started_on

        if not starting_date:
            return

        if not self.deployed_on:
            self.deployed_on = starting_date
            return

        if starting_date > self.deployed_on:
            message = _(
                "Deployment date cannot be earlier that sampling event starting date")
            raise ValidationError(message)

    def validate_recovered_on(self):
        ending_date = self.sampling_event.ended_on

        if not ending_date:
            return

        if not self.recovered_on:
            self.recovered_on = ending_date
            return

        if ending_date < self.recovered_on:
            message = _(
                "Recovery date cannot be latter that sampling event ending date")
            raise ValidationError(message)

    def clean(self):
        try:
            self.validate_licence()
        except ValidationError as error:
            raise ValidationError({'licence': error})

        try:
            sampling_event_type = (
                self.sampling_event.sampling_event_type)
            device_type = (
                self.collection_device.physical_device.device.device_type)

            sampling_event_device_type = (
                sampling_event_type.validate_and_get_device_type(
                    device_type))
        except ValidationError as error:
            raise ValidationError({'physical_device': error})

        if sampling_event_device_type is not None:
            try:
                sampling_event_device_type.validate_metadata(self.metadata)
            except ValidationError as error:
                raise ValidationError({'metadata': error})

        try:
            self.validate_deployed_on()
        except ValidationError as error:
            raise ValidationError({'deployed_on': error})

        try:
            self.validate_recovered_on()
        except ValidationError as error:
            raise ValidationError({'recovered_on': error})

        try:
            physical_device = self.collection_device.physical_device
            physical_device.validate_configuration(self.configuration)
        except ValidationError as error:
            raise ValidationError({'configuration': error})

        if self.licence is not None:
            collection = self.sampling_event.collection
            try:
                collection.validate_and_get_licence(self.licence)
            except ValidationError as error:
                raise ValidationError({'licence': error})

        super().clean()
