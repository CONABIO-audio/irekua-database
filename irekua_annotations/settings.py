from collections import OrderedDict

from irekua_database.settings import *
from irekua_schemas.settings import *
from irekua_terms.settings import *
from irekua_items.settings import *


IREKUA_ANNOTATIONS_APPS = list(
    OrderedDict.fromkeys(
        [
            "irekua_annotations",
        ]
        + IREKUA_ITEMS_APPS
        + IREKUA_TERMS_APPS
        + IREKUA_SCHEMAS_APPS
        + IREKUA_DATABASE_APPS
    )
)
