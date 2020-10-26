from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .collection_items import CollectionItem


class SamplingEventItem(CollectionItem):
    sampling_event = models.ForeignKey(
        'SamplingEvent',
        db_column='sampling_event_id',
        verbose_name=_('sampling event'),
        help_text=_('Sampling event in which this item was captured'),
        on_delete=models.PROTECT,
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Sampling Event Item')

        verbose_name_plural = _('Sampling Event Items')

        ordering = ['-created_on']

    def clean(self):
        super().clean()

        # Check if items of this type are allowed in sampling
        # events of this type.
        self.clean_compatible_item_type()

        # Check that captured on date is within the limits of the
        # sampling event
        self.clean_valid_captured_on()

    def clean_allowed_item_level(self, item_type_config):
        if not item_type_config.sampling_event_item:
            msg = _(
                'Item of type %(item_type)s are cannot be declared at a sampling '
                'event level for collections of type %(collection_type)s')
            params = dict(
                item_type=self.item_type,
                collection_type=item_type_config.collection_type)
            raise ValidationError({'item_type': msg % params})

    def clean_compatible_item_type(self):
        # pylint: disable=no-member
        sampling_event_type = self.sampling_event.sampling_event_type

        try:
            sampling_event_type.validate_item_type(self.item_type)
        except ValidationError as error:
            raise ValidationError({'item_type': error}) from error

    def clean_valid_captured_on(self):
        if self.captured_on is None:
            return

        try:
            # pylint: disable=no-member
            self.sampling_event.validate_date(self.captured_on)

        except ValidationError as error:
            raise ValidationError({'captured_on': error}) from error
