from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase
from irekua_items.models import ItemType


class Visualizer(IrekuaModelBase):
    name = models.CharField(
        max_length=64,
        db_column='name',
        unique=True,
        verbose_name=_('name'),
        help_text=_('Name of visualizer app'),
        blank=False,
        null=False)

    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of the visualizer'),
        blank=True)

    website = models.URLField(
        db_column='website',
        verbose_name=_('website'),
        help_text=_('Link to visualizer website'),
        blank=True)

    item_types = models.ManyToManyField(
        ItemType,
        through='VisualizerItemType',
        through_fields=('visualizer', 'item_type'))

    class Meta:
        verbose_name = _('Visualizer')

        verbose_name_plural = _('Visualizers')

        ordering = ['-created_on']

    def validate_item_type(self, item_type):
        if not self.item_types.filter(pk=item_type.pk).exists():
            msg = _(
                'Items of type %(item_type)s cannot be visualized with visualizer '
                '%(visualizer)s.')
            params = dict(
                item_type=item_type,
                visualizer=self)
            raise ValidationError(msg % params)

    def __str__(self):
        return self.name
