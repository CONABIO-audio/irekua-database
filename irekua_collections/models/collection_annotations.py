from django.db import models
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from irekua_annotations.models import UserAnnotation


class CollectionAnnotation(UserAnnotation):
    collection = models.ForeignKey(
        'Collection',
        db_column='collection_id',
        verbose_name=_('collection'),
        help_text=_('Collection to which this annotation belongs'),
        on_delete=models.PROTECT,
        blank=False,
        null=False)

    collection_metadata = models.JSONField(
        db_column='collection_metadata',
        verbose_name=_('collection metadata'),
        help_text=_('Additional metadata associated to annotation in collection'),
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Collection Annotation')

        verbose_name_plural = _('Collection Annotations')

        ordering = ['-created_on']

    def clean(self):
        super().clean()

        # pylint: disable=no-member
        collection_type = self.collection.collection_type

        # If collection type does not restrict annotation types no further
        # validation is required
        if not collection_type.restrict_annotation_types:
            return

        # Check if this item type is permitted in this collection type
        annotation_type_config = self.clean_allowed_annotation_type(collection_type)

        # Check if collection metadata is valid for this annotation type
        self.clean_valid_collection_metadata(annotation_type_config)

    def clean_allowed_annotation_type(self, collection_type):
        try:
            return collection_type.get_annotation_type(self.annotation_type)

        except ObjectDoesNotExist as error:
            msg = _(
                'Annotations of type %(annotation_type)s are not allowed in '
                'collections of type %(collection_type)s')
            params = dict(
                annotation_type=self.annotation_type,
                collection_type=collection_type)
            raise ValidationError({'annotation_type': msg % params}) from error

    def clean_valid_collection_metadata(self, annotation_type_config):
        try:
            annotation_type_config.validate_metadata(self.collection_metadata)

        except ValidationError as error:
            raise ValidationError({'collection_metadata': str(error)}) from error
