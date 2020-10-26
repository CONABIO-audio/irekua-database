from django.contrib import admin

from irekua_thumbnails import models

from .thumbnails import ItemThumbnailAdmin
from .thumbnail_creators import ThumbnailCreatorAdmin


admin.site.register(models.ItemThumbnail, ItemThumbnailAdmin)
admin.site.register(models.ThumbnailCreator, ThumbnailCreatorAdmin)
