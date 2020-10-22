from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from irekua_database.base import IrekuaModelBaseUser
from irekua_collections.models import Deployment
from irekua_items.models import Item
from irekua_terms.models import Term


class OrganismCapture(IrekuaModelBaseUser):
    organism_capture_type = models.ForeignKey(
        'OrganismCaptureType',
        db_column='organism_capture_type_id',
        verbose_name=_('organism capture type'),
        help_text=_('Capture type'),
        on_delete=models.PROTECT,
        blank=False,
        null=False)

    deployment = models.ForeignKey(
        Deployment,
        db_column='deployment_id',
        verbose_name=_('deployment'),
        help_text=_('Deployed device that capture this organism'),
        on_delete=models.PROTECT,
        blank=False,
        null=False)

    organism = models.ForeignKey(
        'Organism',
        db_column='organism_id',
        verbose_name=_('organism'),
        help_text=_('Captured organism'),
        on_delete=models.PROTECT,
        blank=False,
        null=False)

    metadata = models.JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Additional metadata associated to organism capture'),
        blank=True,
        null=True)

    collection_metadata = models.JSONField(
        db_column='collection_metadata',
        verbose_name=_('collection metadata'),
        help_text=_('Additional metadata associated to organism capture in collection'),
        blank=True,
        null=True)

    labels = models.ManyToManyField(
        Term,
        verbose_name=_('labels'),
        help_text=_('Description of the organism capture'),
        blank=True)

    items = models.ManyToManyField(
        Item,
        verbose_name=_('items'),
        help_text=_('Items associated to this organism'))

    class Meta:
        verbose_name =_('Organism Capture')

        verbose_name_plural =_('Organism Captures')

        ordering = ['-created_on']

    def __str__(self):
        return f'{self.organism_capture_type.name} {self.id}'

    def clean(self):
        super().clean()

        # Check if collection has been configured to use organisms
        organism_config = self.clean_organism_config()

        # Check if collection type allows organisms
        self.clean_collection_type(organism_config)

        # Check that capture type is valid for organism type
        self.clean_compatible_organism_and_capture_type()

        # Check that additional metadata is valid for capture type
        self.clean_metadata()

        # No futher validation is required if organism capture types are not
        # restricted
        if not organism_config.restrict_organism_capture_types:
            return

        # Check organism capture type is allowed in collections of this type
        organism_capture_type_config = self.clean_organism_capture_type(organism_config)

        # Check that additional collection metadata is valid for organism capture type
        self.clean_collection_metadata(organism_capture_type_config)

    def clean_organism_config(self):
        # pylint: disable=no-member
        collection_type = self.collection.collection_type

        try:
            return collection_type.collectiontypeorganismconfig

        except ObjectDoesNotExist as error:
            msg = _('Collections of type %(collection_type)s do not allow organisms.')
            params = dict(collection_type=collection_type)
            raise ValidationError({'collection': msg % params}) from error

    # pylint: disable=no-self-use
    def clean_collection_type(self, organism_config):
        if not organism_config.use_organisms:
            raise ValidationError(_('This collection does not allow organisms'))

    def clean_compatible_organism_and_capture_type(self):
        # pylint: disable=no-member
        if self.organism.organism_type != self.organism_capture_type.organism_type:
            msg = _(
                'Captures of type %(capture_type)s cannot be used on organisms '
                'of type %(organism_type)s')
            # pylint: disable=no-member
            params = dict(
                capture_type=self.organism_capture_type,
                organism_type=self.organism.organism_type)
            raise ValidationError({'organism_capture_type': msg % params})

    def clean_metadata(self):
        try:
            # pylint: disable=no-member
            self.organism_capture_type.validate_metadata(self.metadata)

        except ValidationError as error:
            raise ValidationError({'metadata': error}) from error

    def clean_organism_capture_type(self, organism_config):
        try:
            return organism_config.get_organism_capture_type(self.organism_capture_type)

        except ObjectDoesNotExist as error:
            raise ValidationError({'organism_capture_type': error}) from error

    def clean_collection_metadata(self, organism_capture_type_config):
        try:
            organism_capture_type_config.validate_metadata(self.collection_metadata)

        except ValidationError as error:
            raise ValidationError({'collection_metadata': error}) from error

    def collection(self):
        return self.organism.collection

    def sampling_event(self):
        return self.deployment.samplign_event
