from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .sites import Site


class PointSite(Site):
    geometry = models.PointField(
        blank=True,
        db_column="geo_ref",
        verbose_name=_("geo ref"),
        help_text=_("Georeference of site as Geometry"),
        spatial_index=True,
    )

    latitude = models.FloatField(
        db_column="latitude",
        verbose_name=_("latitude"),
        help_text=_("Latitude of site (in decimal degrees)"),
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        blank=True,
    )

    longitude = models.FloatField(
        db_column="longitude",
        verbose_name=_("longitude"),
        help_text=_("Longitude of site (in decimal degrees)"),
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        blank=True,
    )

    altitude = models.FloatField(
        blank=True,
        db_column="altitude",
        verbose_name=_("altitude"),
        help_text=_("Altitude of site (in meters)"),
        null=True,
    )

    class Meta:
        verbose_name = _("Point Site")

        verbose_name_plural = _("Point Sites")

        ordering = ["-created_on"]

    def clean(self):
        super().clean()

        #  Synchronize point geometry with latitude and longitude fields
        self.sync_coordinates_and_geometry()

    def sync_coordinates_and_geometry(self):
        if self.latitude is not None and self.longitude is not None:
            self.geometry = Point([self.longitude, self.latitude])
            return

        if self.geometry:
            self.latitude = self.geometry.y
            self.longitude = self.geometry.x
            return

        msg = _("No latitude or longitude was provided")
        raise ValidationError({"geometry": msg})
