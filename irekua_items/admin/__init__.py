from django.contrib import admin

from irekua_items import models

from .licences import LicenceAdmin
from .sources import SourceAdmin
from .tags import TagAdmin
from .items import ItemAdmin
from .annotations import AnnotationAdmin
from .annotation_votes import AnnotationVoteAdmin
from .secondary_items import SecondaryItemAdmin
from .thumbnails import ItemThumbnailAdmin


admin.site.register(models.Licence, LicenceAdmin)
admin.site.register(models.Source, SourceAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.ItemThumbnail, ItemThumbnailAdmin)
admin.site.register(models.Annotation, AnnotationAdmin)
admin.site.register(models.AnnotationVote, AnnotationVoteAdmin)
admin.site.register(models.SecondaryItem, SecondaryItemAdmin)
