from collections import OrderedDict

from irekua_database.settings import *
from irekua_schemas.settings import *
from irekua_terms.settings import *
from irekua_items.settings import *
from irekua_devices.settings import *
from irekua_collections.settings import *


IREKUA_ORGANISMS_APPS = list(
    OrderedDict.fromkeys(
        [
            "irekua_organisms",
        ]
        + IREKUA_COLLECTIONS_APPS
        + IREKUA_DEVICES_APPS
        + IREKUA_ITEMS_APPS
        + IREKUA_TERMS_APPS
        + IREKUA_SCHEMAS_APPS
        + IREKUA_DATABASE_APPS
    )
)
