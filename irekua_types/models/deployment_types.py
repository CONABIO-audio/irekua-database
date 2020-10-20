
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase
from irekua_schemas.mixins import MetadataSchemaMixin


class DeploymentType(IrekuaModelBase, MetadataSchemaMixin):
    name = models.CharField(
        max_length=128,
        unique=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name of deployment type'),
        blank=False)

    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of deployment type'),
        blank=True)

    icon = models.ImageField(
        db_column='icon',
        verbose_name=_('icon'),
        help_text=_('Icon for deployment type'),
        upload_to='images/deployment_types/',
        blank=True,
        null=True)

    device_type = models.ForeignKey(
        'DeviceType',
        on_delete=models.PROTECT,
        db_column='device_type_id',
        verbose_name=_('device type'),
        help_text=_(
            'Type of device that can be used in the '
            'deployment of the given type'),
        null=False,
        blank=False)

    restrict_item_types = models.BooleanField(
        db_column='restrict_item_types',
        verbose_name=_('restrict item types'),
        help_text=_(
            'Flag indicating whether to restrict item '
            'types apt for this deployment type'),
        default=False,
        blank=False,
        null=False)

    item_types = models.ManyToManyField(
        'ItemType',
        verbose_name=_('item types'),
        help_text=_('Valid item types for this deployment type'),
        blank=True)

    class Meta:
        verbose_name = _('Deployment Type')

        verbose_name_plural = _('Deployment Types')

        ordering = ['-created_on']

    def __str__(self):
        return self.name

    def validate_device_type(self, device_type):
        if self.device_type != device_type:
            msg = _(
                'The deployment type %(deployment_type)s is for devices of '
                'type %(this)s not %(other)s.')
            params = dict(
                deployment_type=self,
                this=self.device_type,
                other=device_type)
            raise ValidationError(msg % params)

    def validate_item_type(self, item_type):
        if not self.restrict_item_types:
            return

        if not self.item_types.filter(pk=item_type.pk).exists():
            msg = _(
                'This deployment type %(deployment_type)s does not admit '
                'items of type %(item_type)s')
            params = dict(
                deployment_type=str(self),
                item_type=str(item_type))
            raise ValidationError(msg % params)
