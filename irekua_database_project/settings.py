import os
from collections import OrderedDict

from irekua_dev_settings.settings import *
from irekua_database.settings import *
from irekua_schemas.settings import *
from irekua_terms.settings import *
from irekua_geo.settings import *
from irekua_types.settings import *
from irekua_items.settings import *
from irekua_models.settings import *
from irekua_devices.settings import *
from irekua_organisms.settings import *
from irekua_annotators.settings import *
from irekua_visualizers.settings import *
from irekua_collections.settings import *
from irekua_annotations.settings import *
from irekua_thumbnails.settings import *
from irekua_upload.settings import *


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media")

LOCALE_PATHS = [
    os.path.join(BASE_DIR, "irekua_database", "locale"),
]

INSTALLED_APPS = list(
    OrderedDict.fromkeys(
        IREKUA_BASE_APPS
        + IREKUA_DATABASE_APPS
        + IREKUA_SCHEMAS_APPS
        + IREKUA_TERMS_APPS
        + IREKUA_TYPES_APPS
        + IREKUA_DEVICES_APPS
        + IREKUA_GEO_APPS
        + IREKUA_ITEMS_APPS
        + IREKUA_COLLECTIONS_APPS
        + IREKUA_ORGANISMS_APPS
        + IREKUA_MODELS_APPS
        + IREKUA_ANNOTATORS_APPS
        + IREKUA_VISUALIZERS_APPS
        + IREKUA_ANNOTATIONS_APPS
        + IREKUA_THUMBNAILS_APPS
        + IREKUA_UPLOAD_APPS
    )
)

ROOT_URLCONF = "irekua_database_project.urls"

# WSGI_APPLICATION = "irekua_database_project.wsgi"
