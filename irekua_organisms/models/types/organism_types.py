from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from irekua_database.base import IrekuaModelBase
from irekua_schemas.mixins import MetadataSchemaMixin
from irekua_schemas.models import Schema
from irekua_terms.models import TermType
from irekua_items.models import ItemType


class OrganismType(IrekuaModelBase, MetadataSchemaMixin):
    name = models.CharField(
        max_length=64,
        db_column='name',
        verbose_name=_('name'),
        unique=True,
        help_text=_('Name of organism type'),
        blank=False)

    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of organism type'),
        blank=False)

    icon = models.ImageField(
        db_column='icon',
        verbose_name=_('icon'),
        help_text=_('Organism type icon'),
        upload_to='images/organism_types/',
        blank=True,
        null=True)

    term_types = models.ManyToManyField(
        TermType,
        verbose_name=_('term types'),
        help_text=_('Valid term types to describe the organism'),
        blank=True)

    identification_info_schema = models.ForeignKey(
        Schema,
        models.PROTECT,
        related_name='organism_identification_schema',
        db_column='identification_info_schema_id',
        verbose_name=_('identification information schema'),
        help_text=_('JSON Schema for identification information'),
        null=True,
        blank=True)

    is_multi_organism = models.BooleanField(
        db_column='is_multi_organism',
        verbose_name=_('is multi organism'),
        help_text=_(
            'Boolean flag that indicates whether this organism'
            'may be composed by multiple organisms.'),
        blank=False,
        null=False,
        default=False)

    restrict_item_types = models.BooleanField(
        db_column='restrict_item_types',
        verbose_name=_('restrict item types'),
        help_text=_(
            'Flag indicating whether any type of item can be associated '
            'to organisms of this type'),
        default=True,
        null=False,
        blank=True)

    item_types = models.ManyToManyField(
        ItemType,
        verbose_name=_('item types'),
        help_text=_(
            'Types of items that can be associated to '
            'organism of this type.'),
        blank=True)

    class Meta:
        verbose_name =_('Organism Type')

        verbose_name_plural =_('Organism Types')

        ordering = ['-created_on']

    def __str__(self):
        return str(self.name)

    def validate_id_info(self, id_info):
        if self.identification_info_schema is None:
            return

        try:
            self.identification_info_schema.validate(id_info)

        except ValidationError as error:
            msg = _(
                'Invalid identification information for organism '
                'type %(type)s. Error: %(error)s')
            params = dict(type=self.name, error=', '.join(error.messages))
            raise ValidationError(msg % params) from error

    def validate_item_type(self, item_type):
        if not self.restrict_item_types:
            return

        if not self.item_types.filter(id=item_type.id).exists():
            msg = _(
                'Items of type %(item_type)s can not be associated to organism '
                ' of type %(capture_type)s.')
            params = dict(
                item_type=item_type,
                capture_type=self.name)
            raise ValidationError(msg % params)

    def validate_term(self, term):
        if not self.term_types.filter(id=term.term_type.id).exists():
            msg = _(
                'Terms of type %(term_type)s are not allowed for organism '
                ' of type %(capture_type)s. Term: %(term)s')
            params = dict(
                term_type=term.term_type.name,
                capture_type=self.name,
                term=term.value)
            raise ValidationError(msg % params)
