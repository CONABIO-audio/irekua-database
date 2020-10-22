from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase
from irekua_schemas.models import Schema


class TermType(IrekuaModelBase):
    name = models.CharField(
        max_length=128,
        unique=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name for term type'),
        blank=False)

    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of term type'),
        blank=False)

    icon = models.ImageField(
        db_column='icon',
        verbose_name=_('icon'),
        help_text=_('Term type icon'),
        upload_to='images/term_types/',
        blank=True,
        null=True)

    metadata_schema = models.ForeignKey(
        Schema,
        models.PROTECT,
        related_name='term_metadata_schema',
        db_column='metadata_schema_id',
        verbose_name=_('metadata schema'),
        help_text=_('JSON Schema for metadata of term info'),
        null=True,
        blank=True)

    synonym_metadata_schema = models.ForeignKey(
        Schema,
        models.PROTECT,
        related_name='synonym_metadata_schema',
        db_column='synonym_metadata_schema_id',
        verbose_name=_('synonym metadata schema'),
        help_text=_('JSON Schema for metadata of synonym info'),
        null=True,
        blank=True)

    is_categorical = models.BooleanField(
        db_column='is_categorical',
        verbose_name=_('is categorical'),
        help_text=_(
            'Flag indicating whether the term type represents '
            'a categorical variable'),
        default=True,
        blank=False,
        null=False)

    is_numerical = models.BooleanField(
        db_column='is_numerical',
        verbose_name=_('is numerical'),
        help_text=_(
            'Flag indicating whether the term type represents '
            'a numerical (float) variable'),
        default=False,
        blank=False,
        null=False)

    is_integer = models.BooleanField(
        db_column='is_integer',
        verbose_name=_('is integer'),
        help_text=_(
            'Flag indicating whether the term type represents '
            'a integral (int) variable'),
        default=False,
        blank=False,
        null=False)

    is_boolean = models.BooleanField(
        db_column='is_boolean',
        verbose_name=_('is boolean'),
        help_text=_(
            'Flag indicating whether the term type represents '
            'a categorical variable'),
        default=False,
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Term Type')
        verbose_name_plural = _('Term Types')

        ordering = ['name']

    def __str__(self):
        return str(self.name)

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)

        # Check that term type is of one type only (categorical/numeric/boolean/int)
        self.clean_has_only_one_class()

        # Check that no synonym metadata schema was given if not of categorical
        # type.
        self.clean_synonym_metadata()


    def clean_has_only_one_class(self):
        flags = (
            self.is_categorical +
            self.is_numerical +
            self.is_integer +
            self.is_boolean
        )

        if flags != 1:
            msg = _(
                'Term type can only be of one and only one type '
                '(categorical/numerical/integer/boolean)'
            )
            raise ValidationError(msg)

    def clean_synonym_metadata(self):
        if self.is_categorical:
            return

        if self.synonym_metadata_schema is not None:
            msg = _(
                'Non categorical term types cannot have synonyms')
            raise ValidationError(msg)

    def validate_value(self, value):
        if self.is_categorical:
            return self._validate_categorical_value(value)

        if self.is_boolean:
            return self._validate_boolean_value(value)

        if self.is_numerical:
            return self._validate_numerical_value(value)

        if self.is_integer:
            return self._validate_integer_value(value)

        msg = _(
            "Term type %(type)s does not specify if it's of a "
            "categorical/numerical/integer/boolean type"
        )
        params = dict(type=str(self))
        raise ValidationError(msg % params)

    def validate_metadata(self, metadata):
        if self.metadata_schema is None:
            # If no metadata schema for terms was given,
            # any metadata is valid.
            return

        try:
            self.metadata_schema.validate(metadata)

        except ValidationError as error:
            msg = _(
                'Invalid metadata for term of type %(type)s. '
                'Error: %(error)s')
            params = dict(type=str(self), error=str(error))
            raise ValidationError(msg % params) from error

    def validate_synonym_metadata(self, metadata):
        if self.synonym_metadata_schema is None:
            # If no metadata schema for synonyms was given,
            # no metadata is valid.
            msg = _(
                'No synonym metadata schema was given for terms of '
                'type %(type)s, hence synonym metadata is invalid.')
            params = dict(type=str(self))
            raise ValidationError(msg % params)

        try:
            self.synonym_metadata_schema.validate(metadata)

        except ValidationError as error:
            msg = _(
                'Invalid metadata for synonym of terms of type '
                '%(type)s. Error: %(error)s')
            params = dict(type=str(self), error=str(error))
            raise ValidationError(msg % params) from error

    def _validate_numerical_value(self, value):
        if isinstance(value, (float, int)) and not isinstance(value, bool):
            return

        if isinstance(value, str):
            try:
                float(value)
                return
            except ValueError:
                pass

        msg = _(
            'Value %(value)s is invalid for numerical '
            'term of type %(type)s')
        params = dict(value=value, type=str(self))
        raise ValidationError(msg % params)

    def _validate_integer_value(self, value):
        if isinstance(value, int) and not isinstance(value, bool):
            return

        if isinstance(value, float):
            if value % 1 == 0:
                return

        if isinstance(value, str):
            try:
                int(value)
                return
            except ValueError:
                pass

        msg = _(
            'Value %(value)s is invalid for integer '
            'term of type %(type)s')
        params = dict(value=value, type=str(self))
        raise ValidationError(msg % params)

    def _validate_boolean_value(self, value):
        if isinstance(value, bool):
            return

        if isinstance(value, str):
            if value.lower() in ['true', 'false', '0', '1']:
                return

        if isinstance(value, (int, float)):
            if value in [0, 1]:
                return

        msg = _(
            'Value %(value)s is invalid for boolean '
            'term of type %(type)s')
        params = dict(value=value, type=str(self))
        raise ValidationError(msg % params)

    def _validate_categorical_value(self, value):
        if isinstance(value, str):
            return

        msg = _(
            'Value %(value)s is invalid for categorical term '
            'of type %(type)s')
        params = dict(value=value, type=str(self))
        raise ValidationError(msg % params)
