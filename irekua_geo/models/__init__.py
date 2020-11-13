from .linestring_sites import LineStringSite
from .localities import Locality
from .multilinestring_sites import MultiLineStringSite
from .multipoint_sites import MultiPointSite
from .multipolygon_sites import MultiPolygonSite
from .point_sites import PointSite
from .polygon_sites import PolygonSite
from .site_descriptors import SiteDescriptor
from .sites import Site
from .types import LocalityType
from .types import SiteDescriptorType
from .types import SiteType


def get_site_class(geom_type):
    if geom_type == Site.MULTILINESTRING:
        return MultiLineStringSite

    if geom_type == Site.MULTIPOINT:
        return MultiPointSite

    if geom_type == Site.MULTIPOLYGON:
        return MultiPolygonSite

    if geom_type == Site.POINT:
        return PointSite

    if geom_type == Site.POLYGON:
        return PolygonSite

    raise NotImplementedError(f"No site with geometry type {geom_type}")


__all__ = [
    "LineStringSite",
    "Locality",
    "MultiLineStringSite",
    "MultiPointSite",
    "MultiPolygonSite",
    "PointSite",
    "PolygonSite",
    "SiteDescriptor",
    "Site",
    "LocalityType",
    "SiteDescriptorType",
    "SiteType",
    "get_site_class",
]
