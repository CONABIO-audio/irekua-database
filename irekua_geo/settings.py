from collections import OrderedDict

from irekua_database.settings import *
from irekua_schemas.settings import *


IREKUA_GEO_APPS = list(
    OrderedDict.fromkeys(
        [
            "irekua_geo",
        ]
        + IREKUA_SCHEMAS_APPS
        + IREKUA_DATABASE_APPS
    )
)
