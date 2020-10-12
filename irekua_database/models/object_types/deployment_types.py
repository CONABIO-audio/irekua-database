
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_core.utils import validate_JSON_schema
from irekua_core.utils import validate_JSON_instance
from irekua_core.utils import simple_JSON_schema
from irekua_core.models import IrekuaModelBase


class DeploymentType(IrekuaModelBase):
    name = models.CharField(
        max_length=128,
        unique=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name of deployment type'),
        blank=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of deployment type'),
        blank=True)
    icon = models.ImageField(
        db_column='icon',
        verbose_name=_('icon'),
        help_text=_('Icon for deployment type'),
        upload_to='images/deployment_types/',
        blank=True,
        null=True)
    device_type = models.ForeignKey(
        'DeviceType',
        on_delete=models.PROTECT,
        db_column='device_type_id',
        verbose_name=_('device type'),
        help_text=_(
            'Type of device that can be used in the '
            'deployment of the given type'),
        null=False,
        blank=False)
    metadata_schema = models.JSONField(
        db_column='metadata_schema',
        verbose_name=_('metadata schema'),
        help_text=_(
            'JSON schema for metadata associated to device '
            'in sampling event'),
        blank=True,
        null=False,
        default=simple_JSON_schema,
        validators=[validate_JSON_schema])

    class Meta:
        verbose_name = _('Deployment Type')
        verbose_name_plural = _('Deployment Types')

    def validate_metadata(self, metadata):
        try:
            validate_JSON_instance(
                schema=self.metadata_schema,
                instance=metadata)
        except ValidationError as error:
            msg = _(
                'Invalid metadata for device of type %(device)s in sampling'
                'event of type %(sampling_event)s. Error: %(error)')
            params = dict(
                device=str(self.device_type),
                sampling_event=str(self.sampling_event_type),
                error=str(error))
            raise ValidationError(msg, params=params)
