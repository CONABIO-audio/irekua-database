from django.db.models import JSONField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_database.utils import empty_JSON
from irekua_database.base import IrekuaModelBaseUser
from irekua_terms.models import Term
# from selia_annotator.models import AnnotationTool
# from selia_visualizers.models import Visualizer


class Annotation(IrekuaModelBaseUser):
    LOW = 'L'
    MEDIUM = 'M'
    HIGH = 'H'
    CERTAINTY_OPTIONS = [
        (LOW, _('uncertain')),
        (MEDIUM, _('somewhat certain')),
        (HIGH, _('certain')),
    ]
    QUALITY_OPTIONS = [
        (LOW, _('low')),
        (MEDIUM, _('medium')),
        (HIGH, _('high')),
    ]

    annotation_tool = models.ForeignKey(
        'selia_annotator.AnnotationTool',
        on_delete=models.PROTECT,
        db_column='annotation_tool_id',
        verbose_name=_('annotation tool'),
        help_text=_('Annotation tool used when annotating'),
        blank=False)

    visualizer = models.ForeignKey(
        'selia_visualizers.Visualizer',
        on_delete=models.PROTECT,
        db_column='visualizers_id',
        verbose_name=_('visualizer'),
        help_text=_('Visualizer used when annotating'),
        blank=False)

    item = models.ForeignKey(
        'Item',
        db_column='item_id',
        verbose_name=_('item'),
        help_text=_('Annotated item'),
        on_delete=models.PROTECT,
        blank=False)

    event_type = models.ForeignKey(
        'EventType',
        on_delete=models.PROTECT,
        db_column='event_type_id',
        verbose_name=_('event type'),
        help_text=_('Type of event being annotated'),
        blank=False)

    annotation_type = models.ForeignKey(
        'AnnotationType',
        on_delete=models.PROTECT,
        db_column='annotation_type_id',
        verbose_name=_('annotation type'),
        help_text=_('Type of annotation'),
        blank=False)

    annotation = JSONField(
        db_column='annotation',
        verbose_name=_('annotation'),
        default=empty_JSON,
        help_text=_('Information of annotation location within item'),
        blank=True,
        null=False)

    visualizer_configuration = JSONField(
        db_column='visualizer_configuration',
        verbose_name=_('visualizer configuration'),
        default=empty_JSON,
        help_text=_('Configuration of visualizer at annotation creation'),
        blank=True,
        null=False)

    certainty = models.CharField(
        max_length=16,
        db_column='certainty',
        verbose_name=_('certainty'),
        help_text=_(
            'Level of certainty of location or labelling '
            'of annotation'),
        blank=True,
        choices=CERTAINTY_OPTIONS,
        null=True)

    quality = models.CharField(
        db_column='quality',
        verbose_name=_('quality'),
        help_text=_('Quality of item content inside annotation'),
        blank=True,
        max_length=16,
        choices=QUALITY_OPTIONS)

    commentaries = models.TextField(
        db_column='commentaries',
        verbose_name=_('commentaries'),
        help_text=_('Commentaries of annotator'),
        blank=True)

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


# from django.core.exceptions import ValidationError
# from django.db import models
# from django.utils.translation import gettext_lazy as _
#
# from irekua_database.base import IrekuaModelBaseUser
# from irekua_terms.models import Term
#
#
# class Annotation(IrekuaModelBaseUser):
#     item = models.ForeignKey(
#         'Item',
#         db_column='item_id',
#         verbose_name=_('item'),
#         help_text=_('Annotated item'),
#         on_delete=models.PROTECT,
#         blank=False)
#
#     event_type = models.ForeignKey(
#         'EventType',
#         on_delete=models.PROTECT,
#         db_column='event_type_id',
#         verbose_name=_('event type'),
#         help_text=_('Type of event being annotated'),
#         blank=False)
#
#     annotation_type = models.ForeignKey(
#         'AnnotationType',
#         on_delete=models.PROTECT,
#         db_column='annotation_type_id',
#         verbose_name=_('annotation type'),
#         help_text=_('Type of annotation'),
#         blank=False)
#
#     annotation = models.JSONField(
#         db_column='annotation',
#         verbose_name=_('annotation'),
#         help_text=_('Information of annotation location within item'),
#         blank=True,
#         null=False)
#
#     annotation_metadata = models.JSONField(
#         db_column='annotation_metadata',
#         verbose_name=_('annotation metadata'),
#         help_text=_('Additional annotation metadata'),
#         blank=True,
#         null=True)
#
#     event_metadata = models.JSONField(
#         db_column='event_metadata',
#         verbose_name=_('event metadata'),
#         help_text=_('Additional metadata on event occurence'),
#         blank=True,
#         null=True)
#
#     labels = models.ManyToManyField(
#         Term,
#         db_column='labels',
#         verbose_name=_('labels'),
#         help_text=_('Labels associated with annotation'),
#         blank=True)
#
#     class Meta:
#         verbose_name = _('Annotation')
#
#         verbose_name_plural = _('Annotations')
#
#         ordering = ['-modified_on']
#
#         permissions = (
#             ("vote", _("Can vote annotation")),
#         )
#
#     def __str__(self):
#         msg = _('Annotation %(id)s (item %(item_id)s)')
#         params = dict(id=self.id, item_id=self.item)
#         return msg % params
#
#     def clean(self):
#         super().clean()
#
#         # Check event type is valid for item type
#         self.clean_event_type()
#
#         # Check annotation type is valid for event type
#         self.clean_annotation_type()
#
#         # Check annotation is valid for Annotation Type
#         self.clean_annotation()
#
#         # Check annotation metadata is valid
#         self.clean_annotation_metadata()
#
#         # Check event metadata is valid
#         self.clean_event_metadata()
#
#     def clean_event_type(self):
#         try:
#             # pylint: disable=no-member
#             self.item.item_type.validate_event_type(self.event_type)
#
#         except ValidationError as error:
#             raise ValidationError({'event_type': error}) from error
#
#     def clean_annotation_type(self):
#         try:
#             # pylint: disable=no-member
#             self.event_type.validate_annotation_type(self.annotation_type)
#
#         except ValidationError as error:
#             raise ValidationError({'annotation_type': error}) from error
#
#     def clean_annotation(self):
#         try:
#             # pylint: disable=no-member
#             self.annotation_type.validate_annotation(self.annotation)
#
#         except ValidationError as error:
#             raise ValidationError({'annotation': error}) from error
#
#     def clean_annotation_metadata(self):
#         try:
#             # pylint: disable=no-member
#             self.annotation_type.validate_metadata(self.annotation_metadata)
#
#         except ValidationError as error:
#             raise ValidationError({'annotation_metadata': error}) from error
#
#     def clean_event_metadata(self):
#         try:
#             # pylint: disable=no-member
#             self.event_type.validate_metadata(self.event_metadata)
#
#         except ValidationError as error:
#             raise ValidationError({'event_metadata': error}) from error
#
#     def validate_labels(self, labels):
#         for term in labels:
#             term_type = term.term_type.name
#
#             try:
#                 # pylint: disable=no-member
#                 self.event_type.validate_term_type(term_type)
#
#             except ValidationError as error:
#                 msg = _(
#                     'Labels contain a term (of type %(type)s) that is not '
#                     'valid for the event type')
#                 params = dict(type=term_type)
#                 raise ValidationError(msg, params=params) from error
