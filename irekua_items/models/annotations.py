from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBaseUser
from irekua_database.utils import empty_JSON
from irekua_terms.models import Term
from irekua_types.models import EventType
from irekua_types.models import AnnotationType


class Annotation(IrekuaModelBaseUser):
    item = models.ForeignKey(
        'Item',
        db_column='item_id',
        verbose_name=_('item'),
        help_text=_('Annotated item'),
        on_delete=models.PROTECT,
        blank=False)

    event_type = models.ForeignKey(
        EventType,
        on_delete=models.PROTECT,
        db_column='event_type_id',
        verbose_name=_('event type'),
        help_text=_('Type of event being annotated'),
        blank=False)

    annotation_type = models.ForeignKey(
        AnnotationType,
        on_delete=models.PROTECT,
        db_column='annotation_type_id',
        verbose_name=_('annotation type'),
        help_text=_('Type of annotation'),
        blank=False)

    annotation = models.JSONField(
        db_column='annotation',
        verbose_name=_('annotation'),
        default=empty_JSON,
        help_text=_('Information of annotation location within item'),
        blank=True,
        null=False)

    annotation_metadata = models.JSONField(
        db_column='annotation_metadata',
        verbose_name=_('annotation metadata'),
        help_text=_('Additional annotation metadata'),
        blank=True,
        null=True)

    event_metadata = models.JSONField(
        db_column='event_metadata',
        verbose_name=_('event metadata'),
        help_text=_('Additional metadata on event occurence'),
        blank=True,
        null=True)

    labels = models.ManyToManyField(
        Term,
        db_column='labels',
        verbose_name=_('labels'),
        help_text=_('Labels associated with annotation'),
        blank=True)

    class Meta:
        verbose_name = _('Annotation')

        verbose_name_plural = _('Annotations')

        ordering = ['-modified_on']

        permissions = (
            ("vote", _("Can vote annotation")),
        )

    def __str__(self):
        msg = _('Annotation %(id)s (item %(item_id)s)')
        params = dict(id=self.id, item_id=self.item)
        return msg % params

    def clean(self):
        super().clean()

        # Check event type is valid for item type
        try:
            # pylint: disable=no-member
            self.item.item_type.validate_event_type(self.event_type)
        except ValidationError as error:
            raise ValidationError({'event_type': error}) from error

        # Check annotation type is valid for event type
        try:
            self.event_type.validate_annotation_type(self.annotation_type)
        except ValidationError as error:
            raise ValidationError({'annotation_type': error}) from error

        # Check annotation is valid for Annotation Type
        try:
            self.annotation_type.validate_annotation(self.annotation)
        except ValidationError as error:
            raise ValidationError({'annotation': error}) from error

        # Check annotation metadata is valid
        try:
            self.annotation_type.validate_metadata(self.annotation_metadata)
        except ValidationError as error:
            raise ValidationError({'annotation_metadata': error}) from error

        # Check event metadata is valid
        try:
            self.event_type.validate_metadata(self.event_metadata)
        except ValidationError as error:
            raise ValidationError({'event_metadata': error}) from error

        # Labels

    def validate_labels(self, labels):
        for term in labels:
            term_type = term.term_type.name
            try:
                self.event_type.validate_term_type(term_type)
            except ValidationError:
                msg = _(
                    'Labels contain a term (of type %(type)s) that is not '
                    'valid for the event type')
                params = dict(type=term_type)
                raise ValidationError(msg, params=params)
