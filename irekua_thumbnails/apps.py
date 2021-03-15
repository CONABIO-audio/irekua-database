from django.apps import AppConfig


class IrekuaThumbnailsConfig(AppConfig):
    name = "irekua_thumbnails"
    verbose_name = "irekua-thumbnails"

    def ready(self):
        # pylint: disable=import-outside-toplevel,unused-import
        import irekua_thumbnails.signals
