from collections import OrderedDict

from irekua_database.settings import *
from irekua_schemas.settings import *
from irekua_items.settings import *
from irekua_annotations.settings import *


IREKUA_VISUALIZERS_APPS = list(
    OrderedDict.fromkeys(
        [
            "irekua_visualizers",
        ]
        + IREKUA_ANNOTATIONS_APPS
        + IREKUA_ITEMS_APPS
        + IREKUA_SCHEMAS_APPS
        + IREKUA_DATABASE_APPS
    )
)
