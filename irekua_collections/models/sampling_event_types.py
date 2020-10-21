from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from irekua_database.base import IrekuaModelBase
from irekua_schemas.mixins import MetadataSchemaMixin
from irekua_types.models import SiteType
from irekua_types.models import ItemType


class SamplingEventType(IrekuaModelBase, MetadataSchemaMixin):
    name = models.CharField(
        max_length=128,
        unique=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name fo sampling event type'),
        blank=False)

    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of sampling event type'),
        blank=True)

    icon = models.ImageField(
        db_column='icon',
        verbose_name=_('icon'),
        help_text=_('Icon for sampling event type'),
        upload_to='images/sampling_event_types/',
        blank=True,
        null=True)

    restrict_deployment_types = models.BooleanField(
        db_column='restrict_deployment_types',
        verbose_name=_('restrict deployment types'),
        help_text=_(
            'Flag indicating whether to restrict deployment types '
            'associated with this sampling event type'),
        default=False,
        blank=False,
        null=False)

    restrict_site_types = models.BooleanField(
        db_column='restrict_site_types',
        verbose_name=_('restrict site types'),
        help_text=_(
            'Flag indicating whether to restrict site '
            'types associated with this sampling event type'),
        default=False,
        blank=False,
        null=False)

    restrict_item_types = models.BooleanField(
        db_column='restrict_item_types',
        verbose_name=_('restrict item types'),
        help_text=_(
            'Flag indicating whether to restrict item '
            'types apt for this sampling event type'),
        default=False,
        blank=False,
        null=False)

    deployment_types = models.ManyToManyField(
        'DeploymentType',
        verbose_name=_('deployment types'),
        help_text=_('Valid deployment types for this sampling event type'),
        blank=True)

    site_types = models.ManyToManyField(
        SiteType,
        verbose_name=_('site types'),
        help_text=_('Valid site types for this sampling event type'),
        blank=True)

    item_types = models.ManyToManyField(
        ItemType,
        verbose_name=_('item types'),
        help_text=_('Valid item types for this sampling event type'),
        blank=True)

    class Meta:
        verbose_name = _('Sampling Event Type')
        verbose_name_plural = _('Sampling Event Types')
        ordering = ['name']

    def __str__(self):
        return self.name

    def validate_deployment_type(self, deployment_type):
        if not self.restrict_deployment_types:
            return

        if self.deployment_types.filter(pk=deployment_type.pk).exists():
            return

        msg = _(
            'Deployment type %(deployment_type)s is not admitted '
            'for sampling events of type %(sampling_event_type)s.')
        params = dict(
            deployment_type=deployment_type,
            sampling_event_type=self,
        )
        raise ValidationError(msg % params)

    def validate_site_type(self, site_type):
        if not self.restrict_site_types:
            return

        if not self.site_types.filter(pk=site_type.pk).exists():
            msg = _(
                'Site type %(site_type)s is not admitted for '
                'sampling events of type %(sampling_event_type)s')
            params = dict(
                site_type=site_type,
                type=self)
            raise ValidationError(msg % params)

    def validate_item_type(self, item_type):
        if not self.restrict_item_types:
            return

        if not self.item_types.filter(pk=item_type.pk).exists():
            msg = _(
                'Item type %(item_type)s is not admitted for '
                'sampling events of type %(sampling_event_type)s')
            params = dict(
                item_types=item_type,
                type=self)
            raise ValidationError(msg % params)
