from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_items.models import Licence


class CollectionLicence(Licence):
    """Collection Licence Model

    When a collection licence is signed it can be used to
    upload items to a collection. This licence can be reused
    as many times necesary within its collection.
    """
    collection = models.ForeignKey(
        'Collection',
        on_delete=models.CASCADE,
        db_column='collection_id',
        verbose_name=_('collection'),
        help_text=_('Collection to which this licence belongs'),
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Collection Licence')
        verbose_name_plural = _('Collection Licences')
        ordering = ['-created_on']
