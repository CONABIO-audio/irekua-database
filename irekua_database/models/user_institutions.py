from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase


class UserInstitution(IrekuaModelBase):
    institution = models.ForeignKey(
        'Institution',
        models.PROTECT,
        db_column='institution_id',
        verbose_name=_('institution'),
        help_text=_('Institution to which the user belongs'),
        blank=False,
        null=False)
    user = models.ForeignKey(
        'User',
        models.CASCADE,
        db_column='user_id',
        verbose_name=_('user'),
        help_text=_('User that belongs to this institution'),
        blank=False,
        null=False)
    subdependency = models.CharField(
        max_length=256,
        db_column='subdependency',
        verbose_name=_('subdependency'),
        help_text=_('Subdependency at institution to which the user belongs'),
        blank=True,
        null=True)
    position = models.CharField(
        max_length=128,
        db_column='position',
        verbose_name=_('position'),
        help_text=_('Position held by the user in the institution'),
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('User Institution')
        verbose_name_plural = _('User Institutions')

        ordering = [
            '-created_on'
        ]

    def __str__(self):
        if self.position:
            return str(self.position)

        return self.name
