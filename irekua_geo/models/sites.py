from functools import lru_cache

from django.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models import PointField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property

from timezonefinder import TimezoneFinder

from irekua_database.base import IrekuaModelBaseUser


tf = TimezoneFinder()


@lru_cache
def get_timezone(latitude, longitude):
    return tf.timezone_at(lng=longitude, lat=latitude)


class Site(IrekuaModelBaseUser):
    '''
    Site Model

    A site consists of the specification of coordinates. The datum assumed
    is WGS-84. A name for the site can be specified for easier future
    retrieval. Also an optional locality field is added to locate the site within a
    larger area and provide hierarchical organization of sites.

    The creator of the site is registered so that users can search within
    their previously created sites when setting up a new monitoring event.
    '''

    name = models.CharField(
        max_length=128,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name of site (visible only to owner)'),
        blank=True,
        null=True)

    locality = models.ForeignKey(
        'Locality',
        on_delete=models.PROTECT,
        db_column='locality_id',
        verbose_name=_('locality'),
        help_text=_('Name of locality in which the site is located'),
        blank=True,
        null=True)

    geo_ref = PointField(
        blank=True,
        db_column='geo_ref',
        verbose_name=_('geo ref'),
        help_text=_('Georeference of site as Geometry'),
        spatial_index=True)

    latitude = models.FloatField(
        db_column='latitude',
        verbose_name=_('latitude'),
        help_text=_('Latitude of site (in decimal degrees)'),
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        blank=True)

    longitude = models.FloatField(
        db_column='longitude',
        verbose_name=_('longitude'),
        help_text=_('Longitude of site (in decimal degrees)'),
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        blank=True)

    altitude = models.FloatField(
        blank=True,
        db_column='altitude',
        verbose_name=_('altitude'),
        help_text=_('Altitude of site (in meters)'),
        null=True)

    class Meta:
        verbose_name = _('Site')

        verbose_name_plural = _('Sites')

        ordering = ['-created_on']

    def sync_coordinates_and_georef(self):
        if self.latitude is not None and self.longitude is not None:
            self.geo_ref = Point([self.longitude, self.latitude])
            return

        if self.geo_ref:
            self.latitude = self.geo_ref.y
            self.longitude = self.geo_ref.x
            return

        msg = _('No latitude or longitude was provided')
        raise ValidationError({'geo_ref': msg})

    def __str__(self):
        if self.name is not None:
            return self.name
        msg = _('Site %(id)s%')
        params = dict(id=self.id)
        return msg % params

    def clean(self):
        super().clean()

        # Synchronize point geometry with latitude and longitude fields
        self.sync_coordinates_and_georef()

        # Check point is within the declared locality (if any)
        self.validate_locality()

    def validate_locality(self):
        if self.locality is None:
            return

        try:
            # pylint: disable=no-member
            self.locality.validate_point(self.geo_ref)
        except ValidationError as error:
            raise ValidationError({'locality': str(error)}) from error

    @property
    def timezone(self):
        return get_timezone(self.latitude, self.longitude)

    @cached_property
    def items(self):
        from irekua_collections.models import SamplingEventItem

        return SamplingEventItem.objects.filter(
            sampling_event__collection_site__site=self)

    @cached_property
    def sampling_events(self):
        from irekua_collections.models import SamplingEvent

        return SamplingEvent.objects.filter(collection_site__site=self)
