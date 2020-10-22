from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from irekua_database.base import IrekuaModelBase
from irekua_schemas.mixins import MetadataSchemaMixin


class SiteType(IrekuaModelBase, MetadataSchemaMixin):
    name = models.CharField(
        max_length=128,
        unique=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name of site type'),
        blank=False)

    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of site type'),
        blank=False)

    site_descriptor_types = models.ManyToManyField(
        'SiteDescriptorType',
        blank=True)

    class Meta:
        verbose_name = _('Site Type')

        verbose_name_plural = _('Site Types')

        ordering = ['name']

    def __str__(self):
        return self.name

    def validate_descriptor_type(self, descriptor_type):
        if not self.site_descriptor_types.filter(pk=descriptor_type.pk).exists():
            msg = _(
                'Site descriptor type %(descriptor_type)s is not admitted '
                'for site of types %(site_type)s.')
            params = dict(
                descriptor_type=descriptor_type,
                site_type=self)
            raise ValidationError(msg % params)
