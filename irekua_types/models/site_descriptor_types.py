from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase
from irekua_schemas.mixins import MetadataSchemaMixin


class SiteDescriptorType(IrekuaModelBase, MetadataSchemaMixin):
    name = models.CharField(
        max_length=128,
        unique=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name for site descriptor type'),
        blank=False)

    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of site descriptor type'),
        blank=False)

    icon = models.ImageField(
        db_column='icon',
        verbose_name=_('icon'),
        help_text=_('Site descriptor type icon'),
        upload_to='images/site_descriptor_types/',
        blank=True,
        null=True)

    metadata = models.TextField(
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata of site descriptor type'),
        blank=True)

    source = models.URLField(
        db_column='url',
        verbose_name=_('source'),
        help_text=_('Source of information for site descriptor type'),
        blank=True)

    class Meta:
        verbose_name = _('Site Descriptor Type')
        verbose_name_plural = _('Site Descriptor Types')

        ordering = ['name']

    def __str__(self):
        return self.name
