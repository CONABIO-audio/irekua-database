import os

AUTH_USER_MODEL = "irekua_database.User"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


IREKUA_DATABASE_APPS = [
    "irekua_database",
    "django.contrib.postgres",
    "django.contrib.gis",
    "dal",
    "dal_select2",
]


DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "HOST": os.environ.get("IREKUA_DATABASE_HOST", "localhost"),
        "PORT": os.environ.get("IREKUA_DATABASE_PORT", "5432"),
        "NAME": os.environ.get("IREKUA_DATABASE_NAME", "irekua"),
        "USER": os.environ.get("IREKUA_DATABASE_USER", "irekua"),
        "PASSWORD": os.environ.get("IREKUA_DATABASE_PASSWORD", ""),
    }
}
