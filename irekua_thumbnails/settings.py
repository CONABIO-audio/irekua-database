from collections import OrderedDict

from irekua_database.settings import *
from irekua_items.settings import *


IREKUA_THUMBNAILS_APPS = list(
    OrderedDict.fromkeys(
        [
            "irekua_thumbnails",
        ]
        + IREKUA_ITEMS_APPS
        + IREKUA_DATABASE_APPS
    )
)
