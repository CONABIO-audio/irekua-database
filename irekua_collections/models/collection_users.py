from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from irekua_database.utils import empty_JSON
from irekua_database.base import IrekuaModelBaseUser
from irekua_database.models import Role


class CollectionUser(IrekuaModelBaseUser):
    collection = models.ForeignKey(
        'Collection',
        db_column='collection_id',
        verbose_name=_('collection'),
        help_text=_('Collection to which user belongs'),
        on_delete=models.CASCADE,
        blank=False)

    user = models.ForeignKey(
        get_user_model(),
        db_column='user_id',
        verbose_name=_('user'),
        help_text=_('User of collection'),
        on_delete=models.CASCADE,
        blank=False)

    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        db_column='role_id',
        verbose_name=_('role'),
        help_text=_('Role of user in collection'),
        blank=False)

    metadata = models.JSONField(
        blank=True,
        db_column='metadata',
        verbose_name=_('metadata'),
        default=empty_JSON,
        help_text=_('Metadata associated to user in collection'),
        null=True)

    class Meta:
        verbose_name = _('Collection User')

        verbose_name_plural = _('Collection Users')

        unique_together = (
            ('collection', 'user'),
        )

    def __str__(self):
        msg = _('%(user)s (%(role)s)')
        params = dict(user=str(self.user), role=str(self.role))
        return msg % params

    def clean(self):
        super().clean()

        # pylint: disable=no-member
        collection_type = self.collection.collection_type

        # Check if role is registered for collection type
        role_config = self.clean_role(collection_type)

        # Check if additional collection metadata is valid for this site type
        self.clean_metadata(role_config)

    def clean_role(self, collection_type):
        try:
            return collection_type.get_role(self.role)
        except ObjectDoesNotExist as error:
            msg = _(
                'Role %(role)s is not allowed in '
                'collections of type %(collection_type)s')
            params = dict(
                role=self.role,
                collection_type=collection_type)
            raise ValidationError({'role': msg % params}) from error

    def clean_metadata(self, role_config):
        try:
            role_config.validate_metadata(self.metadata)

        except ValidationError as error:
            raise ValidationError({'metadata': str(error)}) from error
