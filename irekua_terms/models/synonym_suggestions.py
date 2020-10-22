from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBaseUser


class SynonymSuggestion(IrekuaModelBaseUser):
    source = models.ForeignKey(
        'Term',
        on_delete=models.CASCADE,
        db_column='source_id',
        verbose_name='source')

    synonym = models.CharField(
        max_length=128,
        db_column='synonym',
        verbose_name=_('synonym'),
        help_text=_('Suggestion of synonym'),
        blank=False)

    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of synonym'),
        blank=True)

    metadata = models.JSONField(
        blank=True,
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to synonym'),
        null=True)

    class Meta:
        ordering = ['-created_on']
        verbose_name = _('Synonym Suggestion')
        verbose_name = _('Synonym Suggestions')

    def __str__(self):
        msg = _('{term} = {suggestion}').format(
            term=str(self.source),
            suggestion=self.synonym)
        return msg

    def clean(self):
        super().clean()

        # Check that synonym metadata is valid for term type
        self.clean_metadata()

    def clean_metadata(self):
        try:
            # pylint: disable=no-member
            self.source.term_type.validate_synonym_metadata(self.metadata)

        except ValidationError as error:
            raise ValidationError({'metadata': error}) from error
