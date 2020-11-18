from collections import OrderedDict

from irekua_database.settings import *
from irekua_schemas.settings import *
from irekua_items.settings import *


IREKUA_DEVICES_APPS = list(
    OrderedDict.fromkeys(
        [
            "irekua_devices",
        ]
        + IREKUA_ITEMS_APPS
        + IREKUA_SCHEMAS_APPS
        + IREKUA_DATABASE_APPS
    )
)
