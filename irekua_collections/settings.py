from collections import OrderedDict

from irekua_database.settings import *
from irekua_schemas.settings import *
from irekua_items.settings import *
from irekua_devices.settings import *
from irekua_geo.settings import *
from irekua_annotations.settings import *


IREKUA_COLLECTIONS_APPS = list(
    OrderedDict.fromkeys(
        [
            "irekua_collections",
        ]
        + IREKUA_ANNOTATIONS_APPS
        + IREKUA_DEVICES_APPS
        + IREKUA_ITEMS_APPS
        + IREKUA_GEO_APPS
        + IREKUA_SCHEMAS_APPS
        + IREKUA_DATABASE_APPS
    )
)
