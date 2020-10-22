from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_collections.models import CollectionItem


class OrganismItem(CollectionItem):
    organism = models.ForeignKey(
        'Organism',
        db_column='organism_id',
        verbose_name=_('organism'),
        help_text=_('Organism to which item belongs'),
        on_delete=models.PROTECT,
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Organism Item')

        verbose_name_plural = _('Organism Items')

        ordering = ['-created_on']

    def clean(self):
        super().clean()

        # Check that organism and item belong to the same collection
        self.clean_same_collection()

        # Check that item type is valid for organism type
        self.clean_compatible_item_type()

    def clean_same_collection(self):
        # pylint: disable=no-member
        if self.collection != self.organism.collection:
            msg = _(
                'Organism %(organism)s does not belong to the collection '
                '%(collection)s')
            params = dict(
                organism=self.organism,
                collection=self.collection)
            raise ValidationError({'organism': msg % params})

    def clean_compatible_item_type(self):
        # pylint: disable=no-member
        organism_type = self.organism.organism_type

        try:
            organism_type.validate_item_type(self.item_type)

        except ValidationError as error:
            raise ValidationError({'item_type': error}) from error
