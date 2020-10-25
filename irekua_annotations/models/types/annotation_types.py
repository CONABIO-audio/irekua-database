from django.db import models

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from irekua_database.base import IrekuaModelBase
from irekua_schemas.models import Schema
from irekua_schemas.mixins import MetadataSchemaMixin


class AnnotationType(IrekuaModelBase, MetadataSchemaMixin):
    name = models.CharField(
        max_length=64,
        unique=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name for type of annotation'))

    description = models.TextField(
        null=False,
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of annotation type'))

    annotation_schema = models.ForeignKey(
        Schema,
        models.PROTECT,
        related_name='annotation_schema',
        db_column='annotation_schema_id',
        verbose_name=_('annotation schema'),
        help_text=_('JSON Schema for annotation info'),
        null=True,
        blank=True)

    icon = models.ImageField(
        db_column='icon',
        upload_to='images/annotation_types/',
        verbose_name=_('icon'),
        help_text=_('Annotation type icon'),
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Annotation Type')

        verbose_name_plural = _('Annotation Types')

        ordering = ['-created_on']

    def __str__(self):
        return self.name

    def validate_annotation(self, annotation):
        try:
            self.annotation_schema.validate(annotation)

        except ValidationError as error:
            msg = _('Invalid annotation for annotation type %(type)s. Error: %(error)s')
            params = dict(type=str(self), error=', '.join(error.messages))
            raise ValidationError(msg, params=params) from error
