from collections import OrderedDict

from irekua_database.settings import *
from irekua_schemas.settings import *
from irekua_annotations.settings import *


IREKUA_ANNOTATORS_APPS = list(
    OrderedDict.fromkeys(
        [
            "irekua_annotators",
        ]
        + IREKUA_ANNOTATIONS_APPS
        + IREKUA_SCHEMAS_APPS
        + IREKUA_DATABASE_APPS
    )
)
