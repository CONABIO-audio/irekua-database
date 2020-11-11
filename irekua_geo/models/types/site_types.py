from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from irekua_database.base import IrekuaModelBase
from irekua_schemas.mixins import MetadataSchemaMixin


class SiteType(IrekuaModelBase, MetadataSchemaMixin):
    name = models.CharField(
        max_length=128,
        unique=True,
        db_column="name",
        verbose_name=_("name"),
        help_text=_("Name of site type"),
        blank=False,
    )

    description = models.TextField(
        db_column="description",
        verbose_name=_("description"),
        help_text=_("Description of site type"),
        blank=False,
    )

    site_descriptor_types = models.ManyToManyField("SiteDescriptorType", blank=True)

    point_site = models.BooleanField(
        default=True,
        db_column="point_site",
        blank=True,
        null=False,
        verbose_name=_("point site"),
        help_text=_("Determines if point sites can be of this type"),
    )

    linestring_site = models.BooleanField(
        default=True,
        db_column="linestring_site",
        blank=True,
        null=False,
        verbose_name=_("linestring site"),
        help_text=_("Determines if linestring sites can be of this type"),
    )

    multilinestring_site = models.BooleanField(
        default=True,
        db_column="multilinestring_site",
        blank=True,
        null=False,
        verbose_name=_("multilinestring site"),
        help_text=_("Determines if multilinestring sites can be of this type"),
    )

    multipoint_site = models.BooleanField(
        default=True,
        db_column="multipoint_site",
        blank=True,
        null=False,
        verbose_name=_("multipoint site"),
        help_text=_("Determines if multipoint sites can be of this type"),
    )

    multipolygon_site = models.BooleanField(
        default=True,
        db_column="multipolygon_site",
        blank=True,
        null=False,
        verbose_name=_("multipolygon site"),
        help_text=_("Determines if multipolygon sites can be of this type"),
    )

    polygon_site = models.BooleanField(
        default=True,
        db_column="polygon_site",
        blank=True,
        null=False,
        verbose_name=_("polygon site"),
        help_text=_("Determines if polygon sites can be of this type"),
    )

    class Meta:
        verbose_name = _("Site Type")

        verbose_name_plural = _("Site Types")

        ordering = ["name"]

    def __str__(self):
        return self.name

    def validate_site_geometry_type(self, site):
        if site.geometry_type == "LineString" and self.linestring_site:
            return

        if site.geometry_type == "MultiLineString" and self.multilinestring_site:
            return

        if site.geometry_type == "MultiPoint" and self.multipoint_site:
            return

        if site.geometry_type == "MultiPolygon" and self.multipolygon_site:
            return

        if site.geometry_type == "Point" and self.point_site:
            return

        if site.geometry_type == "Polygon" and self.polygon_site:
            return

        msg = _(
            "Sites with geometry type %(geometry_type)s cannot be of type "
            "%(site_type)s"
        )
        params = dict(
            geometry_type=site.geometry_type,
            site_type=self,
        )
        raise ValidationError(msg % params)

    def validate_descriptor_type(self, descriptor_type):
        if not self.site_descriptor_types.filter(pk=descriptor_type.pk).exists():
            msg = _(
                "Site descriptor type %(descriptor_type)s is not admitted "
                "for site of types %(site_type)s."
            )
            params = dict(descriptor_type=descriptor_type, site_type=self)
            raise ValidationError(msg % params)
