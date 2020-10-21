import datetime

from pytz import timezone as pytz_timezone

from django.db import models
from django.contrib.gis.db.models import PointField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBaseUser
# from irekua_types.models import DeploymentType


class Deployment(IrekuaModelBaseUser):
    deployment_type = models.ForeignKey(
        'DeploymentType',
        on_delete=models.PROTECT,
        db_column='deployment_type_id',
        verbose_name=_('deployment type'),
        help_text=_('Type of deployment'),
        null=False,
        blank=False)

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

    geo_ref = PointField(
        blank=True,
        null=True,
        db_column='geo_ref',
        verbose_name=_('geo ref'),
        help_text=_('Georeference of deployed device as Geometry'),
        spatial_index=True)

    latitude = models.FloatField(
        db_column='latitude',
        verbose_name=_('latitude'),
        help_text=_('Latitude of deployed device (in decimal degrees)'),
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        null=True,
        blank=True)

    longitude = models.FloatField(
        db_column='longitude',
        verbose_name=_('longitude'),
        help_text=_('Longitude of deployed device (in decimal degrees)'),
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        null=True,
        blank=True)

    altitude = models.FloatField(
        blank=True,
        db_column='altitude',
        verbose_name=_('altitude'),
        help_text=_('Altitude of deployed device (in meters)'),
        null=True)

    collection_device = models.ForeignKey(
        'CollectionDevice',
        db_column='collection_device_id',
        verbose_name=_('collection device'),
        help_text=_('Device being deployed'),
        on_delete=models.PROTECT,
        blank=True,
        null=True)

    commentaries = models.TextField(
        db_column='commentaries',
        verbose_name=_('commentaries'),
        help_text=_('Sampling event commentaries'),
        blank=True)

    metadata = models.JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Additional metadata associated to deployment'),
        blank=True,
        null=True)

    collection_metadata = models.JSONField(
        db_column='collection_metadata',
        verbose_name=_('collection metadata'),
        help_text=_('Additional metadata associated to deployment in collection'),
        blank=True,
        null=True)

    configuration = models.JSONField(
        db_column='configuration',
        verbose_name=_('configuration'),
        help_text=_('Configuration on device when deployed'),
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Deployment')

        verbose_name_plural = _('Deployments')

        unique_together = (
            ('sampling_event', 'collection_device'),
        )

        ordering = ['-created_on']

    def __str__(self):
        msg = _('%(device)s deployed on %(sampling_event)s')
        params = dict(
            device=self.collection_device,
            sampling_event=self.sampling_event)
        return msg % params

    def save(self, *args, **kwargs):
        if self.deployed_on is None:
            # pylint: disable=no-member
            self.deployed_on = self.sampling_event.started_on

        if self.recovered_on is None:
            # pylint: disable=no-member
            self.recovered_on = self.sampling_event.ended_on

        return super().save(*args, **kwargs)

    def clean(self):
        super().clean()

        # Synchronize coordinate fields (altitude, longitude and latitude) with
        # geometry field.
        self.clean_coordinates_and_georef()

        # Check that deployed on datetime is within the sampling event lapse
        self.clean_deployed_on()

        # Check that recovered on date is within the sampling event lapse
        self.clean_recovered_on()

        # Check that recovered_on is not earlier that deployed_on
        self.clean_dates()

        # Check that metadata is valid for deployment type
        self.clean_metadata()

        # Check that configuration information is valid for device
        self.clean_configuration()

        # Check that device and sampling event belong to the same collection
        self.clean_equal_collections()

        # Check that changes made to the deployment-recovery dates do not
        # leave any registered deployment items outside the deployment interval
        self.clean_item_datetimes()

        # pylint: disable=no-member
        collection_type = self.collection_device.collection.collection_type

        # If collection type does not restrict deployment types no further
        # validation is required
        if not collection_type.restrict_deployment_types:
            return

        # Check that deployment type is registered for this collection type
        deployment_type_config = self.clean_deployment_type(collection_type)

        # Check that collection-specific metadata is valid for deployment type
        self.clean_collection_metadata(deployment_type_config)

    def clean_coordinates_and_georef(self):
        if self.latitude is not None and self.longitude is not None:
            self.geo_ref = Point([self.longitude, self.latitude])
            return

        if self.geo_ref:
            self.latitude = self.geo_ref.y
            self.longitude = self.geo_ref.x
            return

        msg = _('Geo reference or longitude-latitude must be provided')
        raise ValidationError({'geo_ref': msg})

    def clean_deployment_type(self, collection_type):
        try:
            return collection_type.get_deployment_type(self.deployment_type)
        except ObjectDoesNotExist as error:
            msg = _(
                'Deployments of type %(deployment_type)s are not allowed in '
                'collections of type %(collection_type)s')
            params = dict(
                deployment_type=self.deployment_type,
                collection_type=collection_type)
            raise ValidationError({'deployment_type': msg % params}) from error

    def clean_metadata(self):
        try:
            self.deployment_type.validate_metadata(self.metadata)
        except ValidationError as error:
            raise ValidationError({'metadata': error}) from error

    def clean_collection_metadata(self, deployment_type_config):
        try:
            deployment_type_config.validate_metadata(self.collection_metadata)
        except ValidationError as error:
            raise ValidationError({'collection_metadata': str(error)}) from error

    def clean_configuration(self):
        # pylint: disable=no-member
        device = self.collection_device.physical_device.device

        try:
            device.validate_configuration(self.configuration)
        except ValidationError as error:
            raise ValidationError({'configuration': error}) from error

    def clean_equal_collections(self):
        # pylint: disable=no-member
        if self.collection_device.collection != self.sampling_event.collection:
            msg = _(
                'The device %(device)s does not belong to the same collection '
                'as the sampling event %(sampling_event)s')
            params = dict(
                device=self.collection_device,
                sampling_event=self.sampling_event)
            raise ValidationError({'collection_device': msg % params})

    def clean_deployed_on(self):
        # pylint: disable=no-member
        starting_date = self.sampling_event.started_on

        if not starting_date:
            return

        if not self.deployed_on:
            self.deployed_on = starting_date
            return

        try:
            # pylint: disable=no-member
            self.sampling_event.validate_date(starting_date)
        except ValidationError as error:
            raise ValidationError({'deployed_on': error}) from error

    def clean_recovered_on(self):
        # pylint: disable=no-member
        ending_date = self.sampling_event.ended_on

        if not ending_date:
            return

        if not self.recovered_on:
            self.recovered_on = ending_date
            return

        try:
            # pylint: disable=no-member
            self.sampling_event.validate_date(ending_date)
        except ValidationError as error:
            raise ValidationError({'recovered_on': error}) from error

    def clean_dates(self):
        if (self.deployed_on is None) or (self.recovered_on is None):
            return

        if self.deployed_on > self.recovered_on:
            msg = _('Device recovery is earlier that its deployment')
            raise ValidationError({'deployed_on': msg})

    def clean_item_datetimes(self):
        start = self.deployed_on if self.deployed_on else None
        end = self.recovered_on if self.recovered_on else None

        if (start is None) and (end is None):
            return

        for item in self.deploymentitem_set.all():
            if not item.captured_on:
                continue

            if start is not None:
                if item.captured_on < start:
                    message = _(
                        'There is an item registered in this deployment that '
                        'was captured earlier that the registered deployment '
                        'date.')
                    raise ValidationError({'deployed_on': message})

            if end is not None:
                if item.captured_on > end:
                    message = _(
                        'There is an item registered in this deployment that '
                        'was captured later that the registered device '
                        'recovery date.')
                    raise ValidationError({'recovered_on': message})

    def collection(self):
        # pylint: disable=no-member
        return self.sampling_event.collection

    def get_best_date_estimate(self, datetime_info, time_zone):
        year = datetime_info.get('year', None)
        month = datetime_info.get('month', None)
        day = datetime_info.get('day', None)
        hour = datetime_info.get('hour', None)
        minute = datetime_info.get('minute', None)
        second = datetime_info.get('second', None)

        if day is None:
            day = self.deployed_on.day

        if month is None:
            month = self.deployed_on.month
            day = 1

        if year is None:
            if self.deployed_on.year != self.recovered_on.year:
                message = _(
                    'No year was provided for date estimation and couldn\'t'
                    ' be inferred from deployment.')
                raise ValidationError(message)

            year = self.deployed_on.year

        if second is None:
            second = self.deployed_on.second

        if minute is None:
            minute = self.deployed_on.minute
            second = self.deployed_on.second

        if hour is None:
            hour = self.deployed_on.hour
            minute = self.deployed_on.minute
            second = self.deployed_on.second

        return datetime.datetime(year, month, day, hour, minute, second, 0, time_zone)

    def get_timezone(self, time_zone=None):
        if time_zone is None:
            # pylint: disable=no-member
            time_zone = self.sampling_event.collection_site.site.timezone

        return pytz_timezone(time_zone)

    def validate_date(self, date_info):
        time_zone = self.get_timezone(time_zone=date_info.get('time_zone', None))
        hdate = self.get_best_date_estimate(date_info, time_zone)
        hdate_up = self.recovered_on.astimezone(time_zone)
        hdate_down = self.deployed_on.astimezone(time_zone)

        if hdate < hdate_down or hdate > hdate_up:
            mssg = _(
                'Date is not within the ranges in which the device was deployed: \n'
                'Deployment: {} \t Recovery: {} \t Date: {}').format(
                    hdate_down,
                    hdate_up,
                    hdate)
            raise ValidationError(mssg)
