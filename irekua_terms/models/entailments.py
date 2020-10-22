from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from irekua_database.base import IrekuaModelBase
from irekua_terms.models.entailment_types import EntailmentType


class Entailment(IrekuaModelBase):
    source = models.ForeignKey(
        'Term',
        related_name='entailment_source',
        db_column='source_id',
        verbose_name=_('source'),
        help_text=_('Source of entailment'),
        on_delete=models.CASCADE,
        blank=False)

    target = models.ForeignKey(
        'Term',
        related_name='entailment_target',
        db_column='target_id',
        verbose_name=_('target'),
        help_text=_('Target of entailment'),
        on_delete=models.CASCADE,
        blank=False)

    metadata = models.JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to entailment'),
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Entailment')

        verbose_name_plural = _('Entailments')

        ordering = ['source']

        unique_together = [
            ['source', 'target']
        ]

    def __str__(self):
        msg = '%(source)s => %(target)s'
        params = dict(
            source=str(self.source),
            target=str(self.target))
        return msg % params

    def clean(self):
        super().clean()

        # Check that entailments between these term types can be made.
        entailment_type = self.check_entailment_type()

        # Check that metadata is valid for this entailment type
        self.check_metadata(entailment_type)

    def check_entailment_type(self):
        try:
            # pylint: disable=no-member
            return EntailmentType.objects.get(
                source_type=self.source.term_type,
                target_type=self.target.term_type)

        except EntailmentType.DoesNotExist as error:
            msg = _(
                'Entailment between types %(source_type)s and '
                '%(target_type)s is not possible')

            # pylint: disable=no-member
            params = dict(
                source_type=self.source.term_type,
                target_type=self.target.term_type)
            raise ValidationError({'target': msg % params}) from error

    def check_metadata(self, entailment_type):
        try:
            entailment_type.validate_metadata(self.metadata)

        except ValidationError as error:
            msg = _('Invalid entailment metadata. Error %(error)s')
            params = dict(error=str(error))
            raise ValidationError({'metadata': msg % params}) from error
