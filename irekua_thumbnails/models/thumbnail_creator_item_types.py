from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase
from irekua_items.models import ItemType



class ThumbnailCreatorItemType(IrekuaModelBase):
    thumbnail_creator = models.ForeignKey(
        'ThumbnailCreator',
        models.CASCADE,
        db_column='thumbnail_creator_id',
        verbose_name=_('thumbnail creator'),
        help_text=_('The thumbnail creator that can process items of this type'),
        null=False,
        blank=False)

    item_type = models.ForeignKey(
        ItemType,
        models.CASCADE,
        db_column='item_type_id',
        verbose_name=_('item type'),
        help_text=_('Item type that can be processed by this thumbnail creator'),
        null=False,
        blank=False)

    is_active = models.BooleanField(
        db_column='is_active',
        verbose_name=_('is active'),
        help_text=_(
            'Indicates wheter this thumbnail creator should be used '
            'as the default thumbnail creator for this item type.'),
        default=True,
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Thumbnail Creator Item Type')

        verbose_name_plural = _('Thumbnail Creator Item Types')

        unique_together = (
            ('thumbnail_creator', 'item_type'),
        )

        ordering = ['-created_on']

    # pylint: disable=signature-differs
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.is_active:
            self._deactivate_others()

    @staticmethod
    def get_thumbnail_creator(item_type):
        return ThumbnailCreatorItemType.objects.get(
            item_type=item_type,
            is_active=True)

    def _deactivate_others(self):
        # pylint: disable=no-member
        (
            ThumbnailCreatorItemType.objects
            .filter(
                item_type=self.item_type,
                is_active=True
            )
            .exclude(pk=self.pk)
            .update(is_active=False)
        )
