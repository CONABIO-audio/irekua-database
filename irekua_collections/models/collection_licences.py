from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
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

    collection_metadata = models.JSONField(
        blank=True,
        db_column='collection_metadata',
        verbose_name=_('collection metadata'),
        help_text=_('Metadata associated with licence within collection'),
        null=True)

    class Meta:
        verbose_name = _('Collection Licence')
        verbose_name_plural = _('Collection Licences')
        ordering = ['-created_on']

    def clean(self):
        super().clean()

        # pylint: disable=no-member
        collection_type = self.collection.collection_type

        # If collection does not restrict licence types
        # no further validation is required
        if not collection_type.restrict_licence_types:
            return

        # Check if licence type is registered for collection type
        licence_type_config = self.clean_licence_type(collection_type)

        # Check if additional collection metadata is valid for this licence type
        self.clean_collection_metadata(licence_type_config)

    def clean_licence_type(self, collection_type):
        try:
            return collection_type.get_licence_type(self.licence_type)

        except ObjectDoesNotExist as error:
            msg = _(
                'Licences of type %(licence_type)s are not allowed in '
                'collections of type %(collection_type)s')
            params = dict(
                licence_type=self.licence_type,
                collection_type=collection_type)
            raise ValidationError({'licence_type': msg % params}) from error

    def clean_collection_metadata(self, licence_type_config):
        try:
            licence_type_config.validate_metadata(self.collection_metadata)

        except ValidationError as error:
            raise ValidationError({'collection_metadata': str(error)}) from error
