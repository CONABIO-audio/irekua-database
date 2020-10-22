import os

from irekua_dev_settings.settings import *
from irekua_database.settings import *
from irekua_schemas.settings import *
from irekua_terms.settings import *
from irekua_types.settings import *
from irekua_devices.settings import *
from irekua_geo.settings import *
from irekua_items.settings import *
from irekua_collections.settings import *
from irekua_organisms.settings import *


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')

LOCALE_PATHS = [os.path.join(BASE_DIR, 'irekua_database', 'locale'), ]

INSTALLED_APPS = (
    IREKUA_BASE_APPS +
    IREKUA_DATABASE_APPS +
    IREKUA_SCHEMAS_APPS +
    IREKUA_TERMS_APPS +
    IREKUA_TYPES_APPS +
    IREKUA_DEVICES_APPS +
    IREKUA_GEO_APPS +
    IREKUA_ITEMS_APPS +
    IREKUA_COLLECTIONS_APPS +
    IREKUA_ORGANISMS_APPS
)
