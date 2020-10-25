from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase
from irekua_items.models import ItemType


class VisualizerItemType(IrekuaModelBase):
    item_type = models.ForeignKey(
        ItemType,
        on_delete=models.CASCADE,
        db_column='item_type_id',
        verbose_name=_('item type'),
        help_text=_('Item type'))

    visualizer = models.ForeignKey(
        'Visualizer',
        on_delete=models.CASCADE,
        db_column='visualizer_id',
        verbose_name=_('visualizer'),
        help_text=_('Visualizer'))

    is_active = models.BooleanField(
        db_column='is_active',
        verbose_name=_('is active'),
        help_text=_(
            'Indicates wheter this visualizer should be used '
            'as the default visualizer of this item type.'),
        default=True,
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Visualizer Item Type')

        verbose_name_plural = _('Visualizer Item Types')

        unique_together = (
            ('item_type', 'visualizer'),
        )

    def deactivate(self):
        self.is_active = False
        self.save()

    def save(self, *args, **kwargs):
        if self.is_active:
            queryset = VisualizerItemType.objects.filter(
                item_type=self.item_type, is_active=True)
            for entry in queryset:
                if entry != self:
                    entry.deactivate()

        super().save(*args, **kwargs)
