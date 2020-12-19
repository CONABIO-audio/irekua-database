import datetime

from pytz import timezone as pytz_timezone
from django.db import models
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.contrib.gis.db.models import PointField
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

from irekua_database.base import IrekuaModelBaseUser


class Deployment(IrekuaModelBaseUser):
    deployment_type = models.ForeignKey(
        "DeploymentType",
        on_delete=models.PROTECT,
        db_column="deployment_type_id",
        verbose_name=_("deployment type"),
        help_text=_("Type of deployment"),
        null=False,
        blank=False,
    )

    sampling_event = models.ForeignKey(
        "SamplingEvent",
        on_delete=models.PROTECT,
        db_column="sampling_event_id",
        verbose_name=_("sampling event"),
        help_text=_("Sampling event in which this device was deployed"),
        blank=False,
        null=False,
    )

    deployed_on = models.DateTimeField(
        db_column="deployed_on",
        verbose_name=_("deployed on"),
        help_text=_("Date at which the device started capturing information."),
        blank=True,
        null=True,
    )

    recovered_on = models.DateTimeField(
        db_column="recovered_on",
        verbose_name=_("recovered on"),
        help_text=_("Date at which the device stoped capturing information."),
        blank=True,
        null=True,
    )

    geo_ref = PointField(
        blank=True,
        null=True,
        db_column="geo_ref",
        verbose_name=_("geo ref"),
        help_text=_("Georeference of deployed device as Geometry"),
        spatial_index=True,
    )

    latitude = models.FloatField(
        db_column="latitude",
        verbose_name=_("latitude"),
        help_text=_("Latitude of deployed device (in decimal degrees)"),
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        null=True,
        blank=True,
    )

    longitude = models.FloatField(
        db_column="longitude",
        verbose_name=_("longitude"),
        help_text=_("Longitude of deployed device (in decimal degrees)"),
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        null=True,
        blank=True,
    )

    altitude = models.FloatField(
        blank=True,
        db_column="altitude",
        verbose_name=_("altitude"),
        help_text=_("Altitude of deployed device (in meters)"),
        null=True,
    )

    collection_device = models.ForeignKey(
        "CollectionDevice",
        db_column="collection_device_id",
        verbose_name=_("collection device"),
        help_text=_("Device being deployed"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    commentaries = models.TextField(
        db_column="commentaries",
        verbose_name=_("commentaries"),
        help_text=_("Sampling event commentaries"),
        blank=True,
    )

    metadata = models.JSONField(
        db_column="metadata",
        verbose_name=_("metadata"),
        help_text=_("Additional metadata associated to deployment"),
        blank=True,
        null=True,
    )

    collection_metadata = models.JSONField(
        db_column="collection_metadata",
        verbose_name=_("collection metadata"),
        help_text=_(
            "Additional metadata associated to deployment in collection"
        ),
        blank=True,
        null=True,
    )

    configuration = models.JSONField(
        db_column="configuration",
        verbose_name=_("configuration"),
        help_text=_("Configuration on device when deployed"),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Deployment")

        verbose_name_plural = _("Deployments")

        unique_together = (("sampling_event", "collection_device"),)

        ordering = ["-created_on"]

    def __str__(self):
        msg = _("%(device)s deployed on %(sampling_event)s")
        params = dict(
            device=self.collection_device,
            sampling_event=self.sampling_event,
        )
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

        # Check that deployment ocurred close enough to the site of the
        # sampling event
        self.clean_deployment_location()

        # Check that deployed on datetime is within the sampling event lapse
        self.clean_valid_deployed_on()

        # Check that recovered on date is within the sampling event lapse
        self.clean_valid_recovered_on()

        #  Check that recovered_on is not earlier that deployed_on
        self.clean_valid_dates()

        # Check that metadata is valid for deployment type
        self.clean_valid_metadata()

        # Check that configuration information is valid for device
        self.clean_valid_configuration()

        # Check that device and sampling event belong to the same collection
        self.clean_equal_collections()

        # Check that changes made to the deployment-recovery dates do not
        # leave any registered deployment items outside the deployment interval
        self.clean_consistent_item_dates()

        # pylint: disable=no-member
        collection_type = self.collection_device.collection.collection_type

        # If collection type does not restrict deployment types no further
        # validation is required
        if not collection_type.restrict_deployment_types:
            return

        # Check that deployment type is registered for this collection type
        deployment_type_config = self.clean_allowed_deployment_type(
            collection_type
        )

        #  Check that collection-specific metadata is valid for deployment type
        self.clean_valid_collection_metadata(deployment_type_config)

    def clean_coordinates_and_georef(self):
        if self.latitude is not None and self.longitude is not None:
            self.geo_ref = Point([self.longitude, self.latitude])
            return

        if self.geo_ref:
            self.latitude = self.geo_ref.y
            self.longitude = self.geo_ref.x
            return

        msg = _("Geo reference or longitude-latitude must be provided")
        raise ValidationError({"geo_ref": msg})

    def clean_deployment_location(self):
        # pylint: disable=no-member
        sampling_event_type = self.sampling_event.sampling_event_type

        if not sampling_event_type.restrict_deployment_positions:
            return

        geometry = self.sampling_event.collection_site.site.geom()
        distance = sampling_event_type.deployment_distance
        if not geometry.buffer(distance).contains(self.geo_ref):
            msg = _(
                "Deployment site is to far away from sampling event site "
                "(> %(distance)s)"
            )
            params = dict(distance=distance)
            raise ValidationError(
                {"latitude": msg % params, "longitude": msg % params}
            )

    def clean_allowed_deployment_type(self, collection_type):
        try:
            return collection_type.get_deployment_type(self.deployment_type)

        except ObjectDoesNotExist as error:
            msg = _(
                "Deployments of type %(deployment_type)s are not allowed in "
                "collections of type %(collection_type)s"
            )
            params = dict(
                deployment_type=self.deployment_type,
                collection_type=collection_type,
            )
            raise ValidationError({"deployment_type": msg % params}) from error

    def clean_valid_metadata(self):
        try:
            # pylint: disable=no-member
            self.deployment_type.validate_metadata(self.metadata)

        except ValidationError as error:
            raise ValidationError({"metadata": error}) from error

    def clean_valid_collection_metadata(self, deployment_type_config):
        try:
            deployment_type_config.validate_metadata(self.collection_metadata)
        except ValidationError as error:
            raise ValidationError(
                {"collection_metadata": str(error)}
            ) from error

    def clean_valid_configuration(self):
        # pylint: disable=no-member
        device = self.collection_device.physical_device.device

        try:
            device.validate_configuration(self.configuration)
        except ValidationError as error:
            raise ValidationError({"configuration": error}) from error

    def clean_equal_collections(self):
        # pylint: disable=no-member
        if self.collection_device.collection != self.sampling_event.collection:
            msg = _(
                "The device %(device)s does not belong to the same collection "
                "as the sampling event %(sampling_event)s"
            )
            params = dict(
                device=self.collection_device,
                sampling_event=self.sampling_event,
            )
            raise ValidationError({"collection_device": msg % params})

    def clean_valid_deployed_on(self):
        # pylint: disable=no-member
        starting_date = self.sampling_event.started_on

        if not starting_date:
            return

        if not self.deployed_on:
            self.deployed_on = starting_date
            return

        try:
            # pylint: disable=no-member
            self.sampling_event.validate_date(self.deployed_on)

        except ValidationError as error:
            raise ValidationError({"deployed_on": error}) from error

    def clean_valid_recovered_on(self):
        # pylint: disable=no-member
        ending_date = self.sampling_event.ended_on

        if ending_date is None:
            return

        if self.recovered_on is None:
            self.recovered_on = ending_date
            return

        try:
            # pylint: disable=no-member
            self.sampling_event.validate_date(self.recovered_on)

        except ValidationError as error:
            raise ValidationError({"recovered_on": error}) from error

    def clean_valid_dates(self):
        if (self.deployed_on is None) or (self.recovered_on is None):
            return

        if self.deployed_on > self.recovered_on:
            msg = _("Device recovery is earlier that its deployment")
            raise ValidationError({"deployed_on": msg})

    def clean_consistent_item_dates(self):
        if self.id is None:
            # Exit early if deployment is being created
            return

        if (self.deployed_on is None) and (self.recovered_on is None):
            return

        queryset = self.collectionitem_set.all()

        if self.deployed_on is not None:
            if queryset.filter(captured_on__lt=self.deployed_on).exists():
                msg = _(
                    "There are items associated to this deployment that "
                    "where captured before the deployment date."
                )
                raise ValidationError({"deployed_on": msg})

        if self.recovered_on is not None:
            if queryset.filter(captured_on__gt=self.deployed_on).exists():
                msg = _(
                    "There are items associated to this deployment that "
                    "where captured after the deployment recovery date."
                )
                raise ValidationError({"deployed_on": msg})

    def collection(self):
        # pylint: disable=no-member
        return self.sampling_event.collection

    def get_best_date_estimate(self, datetime_info, time_zone):
        year = datetime_info.get("year", None)
        month = datetime_info.get("month", None)
        day = datetime_info.get("day", None)
        hour = datetime_info.get("hour", None)
        minute = datetime_info.get("minute", None)
        second = datetime_info.get("second", None)

        if day is None:
            day = self.deployed_on.day

        if month is None:
            month = self.deployed_on.month
            day = 1

        if year is None:
            if self.deployed_on.year != self.recovered_on.year:
                message = _(
                    "No year was provided for date estimation and couldn't"
                    " be inferred from deployment."
                )
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

        return datetime.datetime(
            year, month, day, hour, minute, second, 0, time_zone
        )

    def get_timezone(self, time_zone=None):
        if time_zone is None:
            # pylint: disable=no-member
            time_zone = self.sampling_event.collection_site.site.timezone

        return pytz_timezone(time_zone)

    def validate_date(self, dt):
        if dt < self.deployed_on or self.recovered_on < dt:
            msg = _(
                "Date is not within the ranges in which the device was"
                " deployed: \n Deployment: %(deployed_on)s \t Recovery: "
                "%(recovered_on)s \t Date: %(date)s"
            )
            params = dict(
                deployed_on=self.deployed_on,
                recovered_on=self.recovered_on,
                date=dt,
            )
            raise ValidationError(msg % params)
