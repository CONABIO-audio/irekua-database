from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBaseUser
from irekua_database.models import Institution
from irekua_devices.models import PhysicalDevice
from irekua_geo.models import Site


class Collection(IrekuaModelBaseUser):
    collection_type = models.ForeignKey(
        "CollectionType",
        on_delete=models.PROTECT,
        db_column="collection_type_id",
        verbose_name=_("collection type"),
        help_text=_("Type of collection"),
        blank=False,
        null=False,
    )

    name = models.CharField(
        max_length=128,
        unique=True,
        db_column="name",
        verbose_name=_("name"),
        help_text=_("Name of collection"),
        blank=False,
    )

    description = models.TextField(
        db_column="description",
        verbose_name=_("description"),
        help_text=_("Description of collection"),
        blank=False,
    )

    metadata = models.JSONField(
        db_column="metadata",
        verbose_name=_("metadata"),
        help_text=_("Metadata associated to collection"),
        blank=True,
        null=True,
    )

    institutions = models.ManyToManyField(
        Institution,
        verbose_name=_("institutions"),
        help_text=_("Institutions to which the collection belogs"),
        blank=True,
    )

    logo = models.ImageField(
        db_column="logo",
        verbose_name=_("logo"),
        help_text=_("Logo of data collection"),
        upload_to="images/collections/",
        blank=True,
        null=True,
    )

    physical_devices = models.ManyToManyField(
        PhysicalDevice,
        through="CollectionDevice",
        through_fields=("collection", "physical_device"),
        blank=True,
    )

    sites = models.ManyToManyField(
        Site,
        through="CollectionSite",
        through_fields=("collection", "site"),
        blank=True,
    )

    users = models.ManyToManyField(
        get_user_model(),
        related_name="collection_users",
        through="CollectionUser",
        through_fields=("collection", "user"),
        blank=True,
    )

    administrators = models.ManyToManyField(
        get_user_model(),
        related_name="collection_administrators",
        verbose_name=_("administrators"),
        help_text=_("Administrators of collection"),
        blank=True,
    )

    is_open = models.BooleanField(
        db_column="is_open",
        verbose_name=_("is open"),
        help_text=_(
            "Boolean flag indicating whether contents of the collection " "are public."
        ),
        blank=True,
        null=False,
        default=False,
    )

    class Meta:
        verbose_name = _("Collection")
        verbose_name_plural = _("Collections")

        permissions = (
            ("add_collection_site", _("Can add site to collection")),
            ("add_collection_item", _("Can add item to collection")),
            ("add_collection_device", _("Can add device to collection")),
            (
                "add_collection_sampling_event",
                _("Can add a sampling event to collection"),
            ),
            ("add_collection_user", _("Can add user to collection")),
            ("add_collection_licence", _("Can add licence to collection")),
            (
                "add_collection_annotation",
                _("Can annotate items in collection"),
            ),
            (
                "add_collection_annotation_vote",
                _("Can vote on annotations of items in collection"),
            ),
            ("view_collection_sites", _("Can view sites in collection")),
            ("view_collection_items", _("Can view items in collection")),
            ("view_collection_devices", _("Can view devices in collection")),
            (
                "view_collection_sampling_events",
                _("Can view sampling event in collection"),
            ),
            (
                "view_collection_annotations",
                _("Can view annotations of items in collection"),
            ),
            ("change_collection_sites", _("Can change sites in collection")),
            (
                "change_collection_users",
                _("Can change user info in collection"),
            ),
            ("change_collection_items", _("Can change items in collection")),
            (
                "change_collection_devices",
                _("Can change devices in collection"),
            ),
            (
                "change_collection_annotations",
                _("Can change annotations of items in collection"),
            ),
            (
                "change_collection_sampling_events",
                _("Can change sampling events in collection"),
            ),
            ("download_collection_items", _("Can download annotation items")),
        )

        ordering = ["-created_on"]

    def __str__(self):
        return str(self.name)

    def clean(self):
        super().clean()

        # Check that metadata is valid for this collection type
        self.clean_valid_metadata()

    def clean_valid_metadata(self):
        try:
            # pylint: disable=no-member
            self.collection_type.validate_metadata(self.metadata)

        except ValidationError as error:
            raise ValidationError({"metadata": error}) from error

    def is_admin(self, user):
        queryset = self.administrators.filter(id=user.id)
        return queryset.exists()

    def has_user(self, user):
        return self.users.filter(pk=user.pk).exists()

    def is_user(self, user):
        return self.users.filter(pk=user.pk).exists()

    def has_permission(self, user, codename):
        if user.is_superuser:
            return True

        # Curators have full permissions within collections,
        if user.is_curator:
            return True

        # So do collection type managers,
        if self.collection_type.is_admin(user):
            return True

        # And the collection managers.
        if self.collection.is_admin(user):
            return True

        try:
            role = self.get_user_role(user)
        except self.users.through.DoesNotExist:
            # If user is not part of the collection no
            # permissions are given
            return False

        # Otherwise the role of the user decides if permission is
        # granted
        return role.has_permission(codename)

    def get_user_role(self, user):
        try:
            collection_user = self.users.through.objects.get(collection=self, user=user)
            return collection_user.role

        except self.users.through.DoesNotExist:
            return None

    def update_is_open(self):
        restrictive_licences = self.licence_set.filter(
            is_active=True, licence_type__can_view=False
        )

        self.is_open = not restrictive_licences.exits()
        self.save()

    def can_add_items(self, user):
        """Returns True if user can upload items to this collection"""
        if user.is_superuser:
            return True

        if user.is_curator:
            return True

        if self.collection_type.is_admin(user):
            return True

        if self.collection.is_admin(user):
            return True

        try:
            role = self.get_user_role(user)
        except self.users.through.DoesNotExist:
            # If user is not part of the collection no upload
            # permissions are given
            return False

        return role.has_permission("add_collection_item")