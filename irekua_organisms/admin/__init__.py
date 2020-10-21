from django.contrib import admin

from irekua_organisms import models
from irekua_organisms.admin.collection_type_organism_config import CollectionTypeOrganismConfigAdmin
from irekua_organisms.admin.organism_capture_type import OrganismCaptureTypeAdmin
from irekua_organisms.admin.organism_type import OrganismTypeAdmin
from irekua_organisms.admin.organism import OrganismAdmin
from irekua_organisms.admin.organism_capture import OrganismCaptureAdmin


admin.site.register(
    models.CollectionTypeOrganismConfig,
    CollectionTypeOrganismConfigAdmin)
admin.site.register(
    models.OrganismCaptureType,
    OrganismCaptureTypeAdmin)
admin.site.register(
    models.OrganismType,
    OrganismTypeAdmin)
admin.site.register(
    models.Organism,
    OrganismAdmin)
admin.site.register(
    models.OrganismCapture,
    OrganismCaptureAdmin)
