from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .sampling_event_items import SamplingEventItem


class DeploymentItem(SamplingEventItem):
    deployment = models.ForeignKey(
        'Deployment',
        db_column='deployment_id',
        verbose_name=_('deployment'),
        help_text=_('Deployment of device in which this item was captured'),
        on_delete=models.PROTECT,
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Deployment Item')

        verbose_name_plural = _('Deployment Items')

        ordering = ['-created_on']

    def clean_allowed_item_level(self, item_type_config):
        if not item_type_config.deployment_item:
            msg = _(
                'Item of type %(item_type)s are cannot be declared at a deployment '
                'level for collections of type %(collection_type)s')
            params = dict(
                item_type=self.item_type,
                collection_type=item_type_config.collection_type)
            raise ValidationError({'item_type': msg % params})

    def clean_compatible_item_type(self):
        # pylint: disable=no-member
        deployment_type = self.deployment.deployment_type

        try:
            deployment_type.validate_item_type(self.item_type)
        except ValidationError as error:
            raise ValidationError({'item_type': error}) from error

    def clean_valid_captured_on(self):
        if self.captured_on is None:
            return

        try:
            # pylint: disable=no-member
            self.deployment.validate_date(self.captured_on)

        except ValidationError as error:
            raise ValidationError({'captured_on': error}) from error
