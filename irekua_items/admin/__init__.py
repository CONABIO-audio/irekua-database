from django.contrib import admin

from irekua_items import models

from .licences import LicenceAdmin
from .sources import SourceAdmin
from .tags import TagAdmin
from .items import ItemAdmin
from .secondary_items import SecondaryItemAdmin
from .thumbnails import ItemThumbnailAdmin
from .item_types import ItemTypeAdmin
from .licence_types import LicenceTypeAdmin
from .mime_types import MimeTypeAdmin


admin.site.register(models.MimeType, MimeTypeAdmin)
admin.site.register(models.Licence, LicenceAdmin)
admin.site.register(models.Source, SourceAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.ItemThumbnail, ItemThumbnailAdmin)
admin.site.register(models.SecondaryItem, SecondaryItemAdmin)
admin.site.register(models.ItemType, ItemTypeAdmin)
admin.site.register(models.LicenceType, LicenceTypeAdmin)
