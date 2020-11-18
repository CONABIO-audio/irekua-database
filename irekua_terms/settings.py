from collections import OrderedDict

from irekua_schemas.settings import *
from irekua_database.settings import *


IREKUA_TERMS_APPS = list(
    OrderedDict.fromkeys(
        [
            "irekua_terms",
        ]
        + IREKUA_SCHEMAS_APPS
        + IREKUA_DATABASE_APPS
    )
)
