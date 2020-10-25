from django.db import models
from django.utils.translation import gettext_lazy as _

from .annotations import Annotation


class UserAnnotation(Annotation):
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

    class Meta:
        verbose_name = _('User Annotation')

        verbose_name_plural = _('User Annotations')

        ordering = ['-created_on']
