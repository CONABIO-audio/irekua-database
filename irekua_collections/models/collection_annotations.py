from django.db import models
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from irekua_annotations.models import UserAnnotation


class CollectionAnnotationsManager(models.Manager):
    def open(self):
        """Returns a query set with all annotations that are open access."""
        return self.filter(
            models.Q(item__licence__is_active=False)
            | models.Q(item__licence__licence_type__can_view_annotations=True)
        )

    def user(self, user):
        """Returns a queryset of all the collection annotations a user owns"""
        return self.filter(created_by=user)

    def managed(self, user):
        """Returns a queryset of all annotations that belong to a collection of
        a type managed by the user."""
        managed_collection_types = user.collectiontype_set.all()
        return self.filter(
            collection__collection_type__in=managed_collection_types
        )

    def administered(self, user):
        """Returns a queryset of all annotations that belong to a collection
        administered by the user."""
        administered_collections = user.collection_administrators.all()
        return self.filter(collection__in=administered_collections)

    def shared(self, user):
        """Returns a queryset of all annotations stored in collections to which
        the user has access."""
        collections_with_view_permission = user.collection_users.filter(
            collectionuser__role__permissions__codename="view_collectionannotation"
        )
        return self.filter(collection__in=collections_with_view_permission)

    def can_view(self, user):
        if not user.is_authenticated:
            return self.open()

        if user.is_special:
            return self.all()

        return self.open().union(
            self.user(user),
            self.managed(user),
            self.administered(user),
            self.shared(user),
        )


class CollectionAnnotation(UserAnnotation):
    objects = CollectionAnnotationsManager()

    collection = models.ForeignKey(
        "Collection",
        db_column="collection_id",
        verbose_name=_("collection"),
        help_text=_("Collection to which this annotation belongs"),
        on_delete=models.PROTECT,
        blank=False,
        null=False,
    )

    collection_metadata = models.JSONField(
        db_column="collection_metadata",
        verbose_name=_("collection metadata"),
        help_text=_(
            "Additional metadata associated to annotation in collection"
        ),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Collection Annotation")

        verbose_name_plural = _("Collection Annotations")

        ordering = ["-created_on"]

    def clean(self):
        super().clean()

        # pylint: disable=no-member
        collection_type = self.collection.collection_type

        # If collection type does not restrict annotation types no further
        # validation is required
        if not collection_type.restrict_annotation_types:
            return

        # Check if this item type is permitted in this collection type
        annotation_type_config = self.clean_allowed_annotation_type(
            collection_type
        )

        # Check if collection metadata is valid for this annotation type
        self.clean_valid_collection_metadata(annotation_type_config)

    def clean_allowed_annotation_type(self, collection_type):
        try:
            return collection_type.get_annotation_type(self.annotation_type)

        except ObjectDoesNotExist as error:
            msg = _(
                "Annotations of type %(annotation_type)s are not allowed in "
                "collections of type %(collection_type)s"
            )
            params = dict(
                annotation_type=self.annotation_type,
                collection_type=collection_type,
            )
            raise ValidationError({"annotation_type": msg % params}) from error

    def clean_valid_collection_metadata(self, annotation_type_config):
        try:
            annotation_type_config.validate_metadata(self.collection_metadata)

        except ValidationError as error:
            raise ValidationError(
                {"collection_metadata": str(error)}
            ) from error

    def can_view(self, user):
        if not user.is_authenticated:
            return False

        if user.is_special:
            return True

        # pylint: disable=no-member
        if not self.item.licence.is_active:
            return True

        # pylint: disable=no-member
        if self.item.licence.licence_type.can_view_annotations:
            return True

        if self.created_by == user:
            return True

        if self.collection.collection_type.is_admin(user):
            return True

        if self.collection.is_admin(user):
            return True

        role = self.collection.get_user_role(user)

        if role is None:
            return False

        return role.has_permission("view_collectionannotation")

    def can_change(self, user):
        if not user.is_authenticated:
            return False

        if user.is_superuser or user.is_curator:
            return True

        if self.created_by == user:
            return True

        if self.collection.collection_type.is_admin(user):
            return True

        if self.collection.is_admin(user):
            return True

        role = self.collection.get_user_role(user)

        if role is None:
            return False

        return role.has_permission("change_collectionannotation")

    def can_delete(self, user):
        if not user.is_authenticated:
            return False

        if user.is_superuser or user.is_curator:
            return True

        if self.created_by == user:
            return True

        if self.collection.collection_type.is_admin(user):
            return True

        if self.collection.is_admin(user):
            return True

        role = self.collection.get_user_role(user)

        if role is None:
            return False

        return role.has_permission("delete_collectionannotation")

    def can_vote(self, user):
        if not user.is_authenticated:
            return False

        if self.created_by == user:
            return False

        if user.is_superuser or user.is_curator:
            return True

        # pylint: disable=no-member
        if not self.item.licence.is_active:
            return True

        # pylint: disable=no-member
        if self.item.licence.licence_type.can_vote_annotations:
            return True

        if self.collection.collection_type.is_admin(user):
            return True

        if self.collection.is_admin(user):
            return True

        role = self.collection.get_user_role(user)

        if role is None:
            return False

        return role.has_permission("vote_collectionannotation")
