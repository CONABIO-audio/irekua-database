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

    icon = models.ImageField(
        db_column="icon",
        verbose_name=_("icon"),
        help_text=_("Icon for site type"),
        upload_to="images/site_types/",
        blank=True,
        null=True,
    )

    site_descriptor_types = models.ManyToManyField(
        "SiteDescriptorType",
        blank=True,
        verbose_name=_("site descriptor types"),
        help_text=_(
            "Descriptor types to be used when describing sites of this type"
        ),
    )

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

    can_have_subsites = models.BooleanField(
        default=False,
        db_column="can_have_subsites",
        blank=True,
        null=False,
        verbose_name=_("can have subsites"),
        help_text=_(
            "Determines if sites of this type can have subsites",
        ),
    )

    restrict_subsite_types = models.BooleanField(
        default=False,
        db_column="restrict_subsite_types",
        blank=True,
        null=False,
        verbose_name=_("restrict subsite types"),
        help_text=_(
            "Can any site type be declared as a subsite?",
        ),
    )

    subsite_types = models.ManyToManyField(
        "self",
        blank=True,
        verbose_name=_("subsite types"),
        help_text=_(
            "Site types that can be declared as subsites of sites of this type"
        ),
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

        if (
            site.geometry_type == "MultiLineString"
            and self.multilinestring_site
        ):
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
        if not self.site_descriptor_types.filter(
            pk=descriptor_type.pk
        ).exists():
            msg = _(
                "Site descriptor type %(descriptor_type)s is not admitted "
                "for site of types %(site_type)s."
            )
            params = dict(descriptor_type=descriptor_type, site_type=self)
            raise ValidationError(msg % params)

    def validate_subsite_type(self, site_type):
        if site_type is None:
            return

        if not self.can_have_subsites:
            msg = _("Sites of type %(site_type)s cannot have subsites")
            params = dict(site_type=self)
            raise ValidationError(msg % params)

        if not self.restrict_subsite_types:
            return

        print(site_type, self.subsite_types.all(), self)

        if not self.subsite_types.filter(pk=site_type.pk).exists():
            msg = _(
                "A site of type %(site_type)s cannot be declared as a subsite "
                "of site of type %(self_type)s."
            )
            params = dict(site_type=site_type, self_type=self)
            raise ValidationError(msg % params)
