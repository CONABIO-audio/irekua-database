import os

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_items.models import Item


class CollectionItem(Item):
    upload_to_format = os.path.join(
        'items',
        'collection',
        '{collection}',
        '{hash}{ext}'
    )

    collection = models.ForeignKey(
        'Collection',
        db_column='collection_id',
        verbose_name=_('collection'),
        help_text=_('Collection to which this item belongs'),
        on_delete=models.PROTECT,
        blank=False,
        null=False)

    collection_metadata = models.JSONField(
        db_column='collection_metadata',
        verbose_name=_('collection metadata'),
        help_text=_('Additional metadata associated to site in collection'),
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Collection Item')
        verbose_name_plural = _('Collection Items')

    def clean(self):
        super().clean()

        # pylint: disable=no-member
        collection_type = self.collection.collection_type

        # If collection type does not restrict item types no further
        # validation is required
        if not collection_type.restrict_item_types:
            return

        # Check if this item type is permitted in this collection type
        item_type_config = self.clean_allowed_item_type(collection_type)

        # Check if this type of items can be associated at the correct
        # level
        self.clean_allowed_item_level(item_type_config)

        # Check if collection metadata is valid for this item type
        self.clean_valid_collection_metadata(item_type_config)

    def clean_allowed_item_type(self, collection_type):
        try:
            return collection_type.get_item_type(self.item_type)

        except ObjectDoesNotExist as error:
            msg = _(
                'Item of type %(item_type)s are not allowed in '
                'collections of type %(collection_type)s')
            params = dict(
                item_type=self.item_type,
                collection_type=collection_type)
            raise ValidationError({'item_type': msg % params}) from error

    def clean_allowed_item_level(self, item_type_config):
        if not item_type_config.collection_item:
            msg = _(
                'Item of type %(item_type)s are cannot be declared at a collection '
                'level for collections of type %(collection_type)s')
            params = dict(
                item_type=self.item_type,
                collection_type=item_type_config.collection_type)
            raise ValidationError({'item_type': msg % params})

    def get_upload_to_format_arguments(self):
        return {
            **super().get_upload_to_format_arguments(),
            # pylint: disable=no-member
            'collection': self.collection.id,
        }

    def clean_valid_collection_metadata(self, item_type_config):
        try:
            item_type_config.validate_metadata(self.collection_metadata)

        except ValidationError as error:
            raise ValidationError({'collection_metadata': str(error)}) from error
