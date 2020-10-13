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
        msg = _('Annotation of item %(item_id)s')
        params = dict(item_id=self.item)
        return msg % params

    def clean(self):
        try:
            self.item.validate_and_get_event_type(self.event_type)
        except ValidationError as error:
            raise ValidationError({'event_type': error})

        collection = self.item.sampling_event_device.sampling_event.collection
        try:
            collection.validate_and_get_event_type(self.event_type)
        except ValidationError as error:
            raise ValidationError({'event_type': error})

        try:
            collection.validate_and_get_annotation_type(self.annotation_type)
        except ValidationError as error:
            raise ValidationError({'annotation_type': error})

        try:
            self.annotation_type.validate_annotation(self.annotation)
        except ValidationError as error:
            raise ValidationError({'annotation': error})

        if self.id:
            try:
                self.validate_labels(self.labels.all())
            except ValidationError as error:
                raise ValidationError({'labels': error})

        super(Annotation, self).clean()

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
