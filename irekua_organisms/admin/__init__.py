from django.contrib import admin

from irekua_organisms import models

from irekua_collections.admin.organism_items import OrganismItemAdmin
from .collection_type_organism_config import CollectionTypeOrganismConfigAdmin
from .organism import OrganismAdmin
from .organism_capture import OrganismCaptureAdmin
from .organism_capture_type import OrganismCaptureTypeAdmin
from .organism_type import OrganismTypeAdmin


admin.site.register(
    models.CollectionTypeOrganismConfig,
    CollectionTypeOrganismConfigAdmin,
)

admin.site.register(
    models.OrganismCaptureType,
    OrganismCaptureTypeAdmin,
)

admin.site.register(
    models.OrganismType,
    OrganismTypeAdmin,
)

admin.site.register(
    models.Organism,
    OrganismAdmin,
)

admin.site.register(
    models.OrganismCapture,
    OrganismCaptureAdmin,
)
admin.site.register(
    models.OrganismItem,
    OrganismItemAdmin,
)