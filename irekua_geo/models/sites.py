from functools import lru_cache

from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property
from timezonefinder import TimezoneFinder

from irekua_database.base import IrekuaModelBaseUser


tf = TimezoneFinder()


@lru_cache()
def get_timezone(latitude, longitude):
    return tf.timezone_at(lng=longitude, lat=latitude)


class Site(IrekuaModelBaseUser):
    LINESTRING = "LineString"
    MULTILINESTRING = "MultiLineString"
    MULTIPOINT = "MultiPoint"
    MULTIPOLYGON = "MultiPolygon"
    POINT = "Point"
    POLYGON = "Polygon"
    GEOMETRIES = [
        (LINESTRING, LINESTRING),
        (MULTILINESTRING, MULTILINESTRING),
        (MULTIPOINT, MULTIPOINT),
        (MULTIPOLYGON, MULTIPOLYGON),
        (POINT, POINT),
        (POLYGON, POLYGON),
    ]

    name = models.CharField(
        max_length=128,
        db_column="name",
        verbose_name=_("name"),
        help_text=_("Name of site (visible only to owner)"),
        blank=True,
        null=True,
    )

    localities = models.ManyToManyField(
        "Locality",
        verbose_name=_("locality"),
        help_text=_("Localities in which the site is located"),
        blank=True,
    )

    geometry_type = models.CharField(
        max_length=16,
        choices=GEOMETRIES,
        db_column="geometry_type",
        verbose_name=_("geometry type"),
        help_text=_("Type of geometry of site"),
        null=False,
        blank=False,
    )

    class Meta:
        verbose_name = _("Site")

        verbose_name_plural = _("Sites")

        ordering = ["-created_on"]

        unique_together = [
            ["name", "created_by"],
        ]

    def __str__(self):
        if self.name is not None:
            return self.name

        msg = _("%(geometry_type)s %(id)s")
        params = dict(geometry_type=str(self.geometry_type), id=str(self.id))

        return msg % params

    def clean(self):
        super().clean()

        if self.id is None:
            # Do not run the following validations if
            # object hasn't been created
            return

        # Check that the site falls within the declared localities
        self.clean_localities()

    def geom(self):
        try:
            return self.geometry

        except AttributeError:
            modelname = self.geometry_type.lower() + "site"
            geom_site = getattr(self, modelname)
            return geom_site.geometry

    def clean_localities(self):
        for locality in self.localities.all():
            if locality.geometry.intersects(self.geom()):
                continue

            msg = _(
                "The site %(site)s not does not touch the "
                "locality %(locality)s"
            )
            params = dict(site=self, locality=locality)
            raise ValidationError({"locality": msg % params})

    @property
    def timezone(self):
        geometry = self.geom()
        return get_timezone(
            geometry.centroid.x,
            geometry.centroid.y,
        )

    @cached_property
    def items(self):
        from irekua_collections.models import CollectionItem

        return CollectionItem.objects.filter(collection_site__site=self)

    @cached_property
    def sampling_events(self):
        from irekua_collections.models import SamplingEvent

        return SamplingEvent.objects.filter(collection_site__site=self)
