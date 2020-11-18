from collections import OrderedDict

from irekua_database.settings import *
from irekua_schemas.settings import *


IREKUA_ITEMS_APPS = list(
    OrderedDict.fromkeys(
        [
            "irekua_items",
        ]
        + IREKUA_SCHEMAS_APPS
        + IREKUA_DATABASE_APPS
    )
)
