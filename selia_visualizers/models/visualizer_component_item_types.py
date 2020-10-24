from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase
from irekua_items.models import ItemType


class VisualizerComponentItemType(models.Model):
    item_type = models.ForeignKey(
        ItemType,
        on_delete=models.CASCADE,
        db_column='item_type_id',
        verbose_name=_('item type'),
        help_text=_('Item type'))
    visualizer_component = models.ForeignKey(
        'VisualizerComponent',
        on_delete=models.CASCADE,
        db_column='visualizer_component_id',
        verbose_name=_('visualizer component'),
        help_text=_('Visualizer component'))

    is_active = models.BooleanField(
        db_column='is_active',
        verbose_name=_('is active'),
        help_text=_('Is visualizer app active?'),
        default=True,
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Visualizer Component Item Type')
        verbose_name_plural = _('Visualizer Component Item Types')

        unique_together = (
            ('item_type', 'visualizer_component'),
        )

    def deactivate(self):
        self.is_active = False
        self.save()

    def save(self, *args, **kwargs):
        if self.is_active:
            queryset = VisualizerComponentItemType.objects.filter(
                item_type=self.item_type, is_active=True)
            for entry in queryset:
                if entry != self:
                    entry.deactivate()

        super().save(*args, **kwargs)
