from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property


class User(AbstractUser):
    """
    User Model

    People using irekua must be previously registered and should provide
    minimal personal information. This is to track contributions and to control
    access to data.
    """

    is_developer = models.BooleanField(
        db_column="is_developer",
        verbose_name=_("is developer"),
        help_text=_("Flag to indicate if user is a model developer"),
        blank=False,
        null=False,
        default=False,
    )

    is_curator = models.BooleanField(
        db_column="is_curator",
        verbose_name=_("is curator"),
        help_text=_("Flag to indicate if user is a curator"),
        blank=False,
        null=False,
        default=False,
    )
    is_model = models.BooleanField(
        db_column="is_model",
        verbose_name=_("is model"),
        help_text=_("Flag to indicate if user is an AI model"),
        blank=False,
        null=False,
        default=False,
    )

    institutions = models.ManyToManyField(
        "Institution",
        through="UserInstitution",
        through_fields=("user", "institution"),
        verbose_name=_("user institutions"),
        help_text=_("Institutions to which the user belongs"),
    )

    class Meta:
        verbose_name = _("User")

        verbose_name_plural = _("Users")

        unique_together = [
            [
                "email",
            ],
        ]

    @property
    def is_special(self):
        return (
            self.is_developer
            | self.is_curator
            | self.is_model
            | self.is_superuser
        )

    #  TODO: Remove methods that import models from derived irekua-modules.
    @cached_property
    def is_collection_type_admin(self):
        return self.collectiontype_set.exists()

    @cached_property
    def admin_collections(self):
        from irekua_collections.models import Collection

        return Collection.objects.filter(administrators=self)

    @cached_property
    def managed_collections(self):
        from irekua_collections.models import Collection

        return Collection.objects.filter(collection_type__administrators=self)

    def collections_with_permissions(self, codename):
        from irekua_collections.models import Collection

        memberships = self.collectionuser_set.filter(
            role__permissions__codename=codename
        )
        return Collection.objects.filter(collectionuser__in=memberships)
