from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase


class Synonym(IrekuaModelBase):
    source = models.ForeignKey(
        'Term',
        related_name='synonym_source',
        on_delete=models.CASCADE,
        db_column='source_id',
        verbose_name=_('source'),
        help_text=_('Reference to the source of synonym'),
        blank=False)

    target = models.ForeignKey(
        'Term',
        related_name='synonym_target',
        on_delete=models.CASCADE,
        db_column='target_id',
        verbose_name=_('target'),
        help_text=_('Reference to the target of the synonym'),
        blank=False)

    metadata = models.JSONField(
        blank=True,
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to the synonym'),
        null=True)

    class Meta:
        verbose_name = _('Synonym')

        verbose_name_plural = _('Synonyms')

        unique_together = [
            ['source', 'target']
        ]

        ordering = ['source']

    def __str__(self):
        msg = '%(source)s = %(target)s'
        params = dict(
            source=str(self.source),
            target=str(self.target))
        return msg % params

    def clean(self):
        super().clean()

        # Check that both terms are of the same type.
        self.clean_same_type()

        # Check that the term type is categorical. It doesn't make sense to
        # create synonyms between integer/boolean/numeric terms.
        self.clean_is_categorical()

        # Check that metadata is valid for term type
        self.clean_metadata()

    def clean_same_type(self):
        # pylint: disable=no-member
        if self.source.term_type != self.target.term_type:
            msg = _('Source and target terms are not of the same type')
            raise ValidationError({'target': msg})

    def clean_is_categorical(self):
        # pylint: disable=no-member
        if not self.source.term_type.is_categorical:
            msg = _('Cannot create synonyms between non-categorical terms')
            raise ValidationError({'source': msg})

    def clean_metadata(self):
        try:
            # pylint: disable=no-member
            self.source.term_type.validate_synonym_metadata(self.metadata)

        except ValidationError as error:
            raise ValidationError({'metadata': error}) from error
