from collections import OrderedDict

from irekua_database.settings import *


IREKUA_SCHEMAS_APPS = list(
    OrderedDict.fromkeys(
        [
            "irekua_schemas",
        ]
        + IREKUA_DATABASE_APPS
    )
)
