from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Schema


class MetadataSchemaMixin(models.Model):
    metadata_schema = models.ForeignKey(
        Schema,
        models.PROTECT,
        related_name='%(class)s_metadata_schema',
        db_column='metadata_schema_id',
        verbose_name=_('metadata schema'),
        help_text=_('JSON Schema for additional metadata'),
        null=True,
        blank=True)

    class Meta:
        abstract = True

    def validate_metadata(self, metadata):
        if self.metadata_schema is None:
            return

        try:
            self.metadata_schema.validate(metadata)
        except ValidationError as error:
            msg = _('Invalid metadata for %(type)s. Error: %(error)s')
            params = dict(type=str(self), error=', '.join(error.messages))
            raise ValidationError(msg, params=params) from error
