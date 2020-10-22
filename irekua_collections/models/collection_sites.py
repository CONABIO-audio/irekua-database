from django.db import models
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBaseUser
from irekua_geo.models import SiteType
from irekua_geo.models import SiteDescriptor
from irekua_geo.models import Site


class CollectionSite(IrekuaModelBaseUser):
    site_type = models.ForeignKey(
        SiteType,
        on_delete=models.PROTECT,
        db_column='site_type',
        verbose_name=_('site type'),
        help_text=_('Type of site'),
        blank=False,
        null=False)

    site = models.ForeignKey(
        Site,
        on_delete=models.PROTECT,
        db_column='site_id',
        verbose_name=_('site'),
        help_text=_('Reference to Site'),
        blank=False,
        null=False)

    collection = models.ForeignKey(
        'Collection',
        on_delete=models.CASCADE,
        db_column='collection_id',
        verbose_name=_('collection'),
        help_text=_('Collection to which the site belongs'),
        blank=False,
        null=False)

    metadata = models.JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to site'),
        blank=True,
        null=True)

    collection_metadata = models.JSONField(
        db_column='collection_metadata',
        verbose_name=_('collection metadata'),
        help_text=_('Additional metadata associated to site in collection'),
        blank=True,
        null=True)

    collection_name = models.CharField(
        max_length=64,
        db_column='collection_name',
        verbose_name=_('collection name'),
        help_text=_('Name of site within the collection (visible to all collection users)'),
        blank=True)

    site_descriptors = models.ManyToManyField(
        SiteDescriptor,
        blank=True)

    class Meta:
        verbose_name = _('Collection Site')

        verbose_name_plural = _('Collection Sites')

        unique_together = (
            ('collection', 'site'),
            ('collection', 'collection_name'),
        )

    def __str__(self):
        if self.collection_name:
            return self.collection_name

        if self.site.name:
            return self.site.name

        msg = _('Site %(id)s')
        params = dict(id=str(self.id))
        return msg % params

    def clean(self):
        super().clean()

        # Check that metadata is valid for site type
        self.clean_metadata()

        # pylint: disable=no-member
        collection_type = self.collection.collection_type

        # If collection does not restrict site types
        # no further validation is required
        if not collection_type.restrict_site_types:
            return

        # Check if site type is registered for collection type
        site_type_config = self.clean_site_type(collection_type)

        # Check if additional collection metadata is valid for this site type
        self.clean_collection_metadata(site_type_config)

    def clean_metadata(self):
        try:
            self.site_type.validate_metadata(self.metadata)

        except ValidationError as error:
            raise ValidationError({'metadata': str(error)}) from error

    def clean_site_type(self, collection_type):
        try:
             return collection_type.get_site_type(self.site_type)
        except ObjectDoesNotExist as error:
            msg = _(
                'Sites of type %(site_type)s are not allowed in '
                'collections of type %(collection_type)s')
            params = dict(
                site_type=self.site_type,
                collection_type=collection_type)
            raise ValidationError({'site_type': msg % params}) from error

    def clean_collection_metadata(self, site_type_config):
        try:
            site_type_config.validate_metadata(self.collection_metadata)

        except ValidationError as error:
            raise ValidationError({'collection_metadata': str(error)}) from error

    def validate_descriptor(self, descriptor):
        if self.id is None:
            # Exit early if instance is being created
            return

        self.site_type.validate_descriptor_type(descriptor.descriptor_type)

    @property
    def items(self):
        from irekua_collections.models import SamplingEventItemItem
        return SamplingEventItemItem.objects.filter(
            sampling_event__collection_site=self)

    @cached_property
    def deployments(self):
        from irekua_collections.models import Deployment
        return Deployment.objects.filter(sampling_event__collection_site=self)
