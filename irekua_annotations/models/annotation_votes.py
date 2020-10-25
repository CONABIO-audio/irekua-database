from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_terms.models import Term
from irekua_database.base import IrekuaModelBaseUser


class AnnotationVote(IrekuaModelBaseUser):
    annotation = models.ForeignKey(
        'Annotation',
        on_delete=models.CASCADE,
        db_column='annotation_id',
        verbose_name=_('annotation'),
        help_text=_('Reference to annotation being voted'),
        blank=False,
        null=False)

    incorrect_geometry = models.BooleanField(
        db_column='incorrect_geometry',
        verbose_name=_('incorrect geometry'),
        help_text=_('Is the annotation geometry incorrect?'),
        blank=True,
        default=False,
        null=False)

    labels = models.ManyToManyField(
        Term,
        db_column='labels',
        verbose_name=_('labels'),
        help_text=_('Labels associated with annotation'),
        blank=True)

    class Meta:
        verbose_name = _('Annotation Vote')

        verbose_name_plural = _('Annotation Votes')

        unique_together = [
            ['annotation', 'created_by'],
        ]

        ordering = ['-created_on']

    def __str__(self):
        msg = _('Vote %(id)s on annotation %(annotation)s')
        # pylint: disable=no-member
        params = dict(
            id=self.id,
            annotation=self.annotation.id)
        return msg % params

    def clean(self):
        super().clean()

        # Check that labels are valid for this annotation.
        self.clean_labels()

    def clean_labels(self):
        if not self.id:
            # Exit early if AnnotationVote is being created
            return

        try:
            self.validate_labels(self.labels.all())

        except ValidationError as error:
            raise ValidationError({'labels': error}) from error

    def validate_labels(self, labels):
        for term in labels:
            term_type = term.term_type.name

            try:
                # pylint: disable=no-member
                self.annotation.event_type.validate_term_type(term_type)

            except ValidationError as error:
                msg = _(
                        'Labels contain a term (of type %(type)s) that is not '
                        'valid for the event type')
                params = dict(type=term_type)
                raise ValidationError(msg, params=params) from error
