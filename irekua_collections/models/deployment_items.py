from django.db import models
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
