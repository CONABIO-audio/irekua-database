from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db.models import MultiPolygonField

from irekua_database.base import IrekuaModelBase


class Locality(IrekuaModelBase):
    name = models.CharField(
        max_length=128,
        db_column='name',
        help_text=_('Name of locality'),
        blank=False)

    description = models.TextField(
        blank=True,
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of the locality'))

    locality_type = models.ForeignKey(
        'LocalityType',
        on_delete=models.PROTECT,
        db_column='locality_type_id',
        verbose_name=_('locality type'),
        help_text=_('Type of locality'),
        blank=False,
        null=False)

    geometry = MultiPolygonField(
        blank=True,
        db_column='geometry',
        verbose_name=_('geometry'),
        help_text=_('Geometry of locality'),
        spatial_index=True)

    metadata = models.JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to locality'),
        blank=True,
        null=True)

    is_part_of = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True)

    class Meta:
        verbose_name = _('Locality')
        verbose_name_plural = _('Localities')

        ordering = ['-name']

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)

        # Check metdata is valid for locality type
        self.clean_metadata()

    def clean_metadata(self):
        try:
            # pylint: disable=no-member
            self.locality_type.validate_metadata(self.metadata)

        except ValidationError as error:
            raise ValidationError({'metadata': error}) from error

    def validate_point(self, point):
        # pylint: disable=no-member
        if not self.geometry.contains(point):
            msg = _(
                "Point is not contained within the locality's geometry")
            raise ValidationError(msg)

    def __str__(self):
        return '{locality_type}: {name}'.format(
            locality_type=self.locality_type,
            name=self.name)
