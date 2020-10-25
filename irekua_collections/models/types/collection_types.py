from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase
from irekua_database.models import Role

from irekua_items.models import types as item_type_models
from irekua_devices.models import types as device_type_models
from irekua_geo.models import types as site_type_models
from irekua_annotations.models import types as annotation_type_models

from irekua_collections.mixins import CollectionMetadataSchemaMixin


class CollectionType(IrekuaModelBase, CollectionMetadataSchemaMixin):
    """
    *Collection types* function as a templates for collection creation. Its
    utility stems from the fact that the configuration of a collection can be
    a tedious process and usually some preconfigured option suffices for the
    need in hand. A collection type contains all collection behaviour
    configuration. This amounts to the following specifications:

    1. Metadata:
        Any collection created with this template must provide further metadata
        as specified by the collection type metadata schema.

    2. Creation Configuration:
        Sometimes collection types can also serve to categorize collections and
        thus creation of collections of this types must not be free. A flag
        (anyone_can_create) has been included to indicate whether any user can
        create a collection of this type. If creation is restricted, then
        administrators must be specified. Administrators will have all permissions
        on children collections, and they alone have the permissions to create
        collections of this type.

        # TODO
    """
    name = models.CharField(
        max_length=128,
        unique=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name of collection type'),
        blank=False)

    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of collection type'),
        blank=False)

    logo = models.ImageField(
        upload_to='images/collection_types/',
        db_column='logo',
        verbose_name=_('logo'),
        help_text=_('Logo of collection type'),
        blank=True,
        null=True)

    anyone_can_create = models.BooleanField(
        db_column='anyone_can_create',
        verbose_name=_('anyone can create'),
        help_text=_(
            'Boolean flag indicating wheter any user can '
            'create collections of this type'),
        blank=True,
        default=False,
        null=False)

    administrators = models.ManyToManyField(
        get_user_model(),
        verbose_name=_('administrators'),
        help_text=_(
            'Administrators of this collection type. Administrators can '
            'create collections of this type'),
        blank=True)

    restrict_site_types = models.BooleanField(
        db_column='restrict_site_types',
        verbose_name=_('restrict site types'),
        help_text=_(
            'Flag indicating whether types of sites are restricted to '
            'registered ones'),
        default=True,
        null=False,
        blank=True)

    restrict_annotation_types = models.BooleanField(
        db_column='restrict_annotation_types',
        verbose_name=_('restrict annotation types'),
        help_text=_(
            'Flag indicating whether types of annotations are restricted '
            'to registered ones'),
        default=True,
        null=False,
        blank=True)

    restrict_item_types = models.BooleanField(
        db_column='restrict_item_types',
        verbose_name=_('restrict item types'),
        help_text=_(
            'Flag indicating whether types of items are restricted to '
            'registered ones'),
        default=True,
        null=False,
        blank=True)

    restrict_licence_types = models.BooleanField(
        db_column='restrict_licence_types',
        verbose_name=_('restrict licence types'),
        help_text=_(
            'Flag indicating whether types of licences are restricted to '
            'registered ones'),
        default=True,
        null=False,
        blank=True)

    restrict_device_types = models.BooleanField(
        db_column='restrict_device_types',
        verbose_name=_('restrict device types'),
        help_text=_(
            'Flag indicating whether types of devices are restricted to '
            'registered ones'),
        default=True,
        null=False,
        blank=True)

    restrict_event_types = models.BooleanField(
        db_column='restrict_event_types',
        verbose_name=_('restrict event types'),
        help_text=_(
            'Flag indicating whether types of events are restricted to '
            'registered ones'),
        default=True,
        null=False,
        blank=True)

    restrict_sampling_event_types = models.BooleanField(
        db_column='restrict_sampling_event_types',
        verbose_name=_('restrict sampling event types'),
        help_text=_(
            'Flag indicating whether types of sampling events are restricted '
            'to registered ones'),
        default=True,
        null=False,
        blank=True)

    restrict_deployment_types = models.BooleanField(
        db_column='restrict_deployment_types',
        verbose_name=_('restrict deployment types'),
        help_text=_(
            'Flag indicating whether types of deployment are restricted '
            'to registered ones'),
        default=True,
        null=False,
        blank=True)

    site_types = models.ManyToManyField(
        site_type_models.SiteType,
        through='CollectionTypeSiteType',
        through_fields=('collection_type', 'site_type'),
        verbose_name=_('site types'),
        help_text=_('Types of sites valid for collections of type'),
        blank=True)

    annotation_types = models.ManyToManyField(
        annotation_type_models.AnnotationType,
        through='CollectionTypeAnnotationType',
        through_fields=('collection_type', 'annotation_type'),
        verbose_name=_('annotation types'),
        help_text=_('Types of annotations valid for collections of type'),
        blank=True)

    licence_types = models.ManyToManyField(
        item_type_models.LicenceType,
        through='CollectionTypeLicenceType',
        through_fields=('collection_type', 'licence_type'),
        verbose_name=_('licence types'),
        help_text=_('Types of licences valid for collections of type'),
        blank=True)

    event_types = models.ManyToManyField(
        annotation_type_models.EventType,
        through='CollectionTypeEventType',
        through_fields=('collection_type', 'event_type'),
        verbose_name=_('event types'),
        help_text=_('Types of events valid for collections of type'),
        blank=True)

    sampling_event_types = models.ManyToManyField(
        'SamplingEventType',
        through='CollectionTypeSamplingEventType',
        through_fields=('collection_type', 'sampling_event_type'),
        verbose_name=_('sampling event types'),
        help_text=_('Types of sampling events valid for collections of type'),
        blank=True)

    item_types = models.ManyToManyField(
        item_type_models.ItemType,
        through='CollectionTypeItemType',
        through_fields=('collection_type', 'item_type'),
        verbose_name=_('item types'),
        help_text=_('Types of items valid for collections of type'),
        blank=True)

    device_types = models.ManyToManyField(
        device_type_models.DeviceType,
        through='CollectionTypeDeviceType',
        through_fields=('collection_type', 'device_type'),
        verbose_name=_('device types'),
        help_text=_('Types of devices valid for collections of type'),
        blank=True)

    deployment_types = models.ManyToManyField(
        'DeploymentType',
        through='CollectionTypeDeploymentType',
        through_fields=('collection_type', 'deployment_type'),
        verbose_name=_('device types'),
        help_text=_('Types of deployments valid for collections of type'),
        blank=True)

    roles = models.ManyToManyField(
        Role,
        through='CollectionTypeRole',
        through_fields=('collection_type', 'role'),
        verbose_name=_('roles'),
        help_text=_('Roles valid for collections of type'),
        blank=True)

    class Meta:
        verbose_name = _('Collection Type')
        verbose_name_plural = _('Collection Types')
        ordering = ['name']

    def __str__(self):
        return str(self.name)

    def get_device_type(self, device_type):
        return self.device_types.through.objects.get(
            collection_type=self,
            device_type=device_type,
        )

    def get_site_type(self, site_type):
        return self.site_types.through.objects.get(
            collection_type=self,
            site_type=site_type,
        )

    def get_annotation_type(self, annotation_type):
        return self.annotation_types.through.objects.get(
            collection_type=self,
            annotation_type=annotation_type,
        )

    def get_event_type(self, event_type):
        return self.event_types.through.objects.get(
            collection_type=self,
            event_type=event_type,
        )

    def get_sampling_event_type(self, sampling_event_type):
        return self.sampling_event_types.through.objects.get(
            collection_type=self,
            sampling_event_type=sampling_event_type,
        )

    def get_item_type(self, item_type):
        return self.item_types.through.objects.get(
            collection_type=self,
            item_type=item_type,
        )

    def get_role(self, role):
        return self.roles.through.objects.get(
            collection_type=self,
            role=role,
        )

    def get_deployment_type(self, deployment_type):
        return self.deployment_types.through.objects.get(
            collection_type=self,
            deployment_type=deployment_type,
        )

    def is_admin(self, user):
        return self.administrators.filter(id=user.id).exists()

    @property
    def users(self):
        from irekua_collections.models import CollectionUser
        return CollectionUser.objects.filter(
            collection__collection_type=self)

    @property
    def collections(self):
        from irekua_collections.models import Collection
        return Collection.objects.filter(collection_type=self)

    @property
    def items(self):
        from irekua_collections.models import CollectionItem
        return CollectionItem.objects.filter(collection__collection_type=self)

    @property
    def annotations(self):
        from irekua_items.models import Annotation
        return Annotation.objects.filter(
            item__collectionitem__collection__collection_type=self
        )

    @property
    def last_item(self):
        return self.items.order_by('-created_on').first()

    @property
    def last_annotation(self):
        return self.annotations.order_by('-created_on').first()
