from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from irekua_database.base import IrekuaModelBaseUser


class Licence(IrekuaModelBaseUser):
    '''
    Licence Model

    A licence is a legal document expressing detail about ownership and
    permissions of any items to which the licence is attached. The licences
    are valid until specified, and any item licenced by and outdated licence
    will be of open access.

    The licence type (:model:`irekua_database.LicenceType`) contains all details about permissions and also holds a
    template document to be filled whenever creating a new licence of such
    type.

    A single licence can only apply to items (:model:`irekua_database.Item`) within the same collection
    (:model:`irekua_database.Collection`), therefore a reference to the collection to
    which the licence belongs is stored. This facilitates the process of
    attaching a licence to uploaded items, since the number of
    licences belonging to a single collection is recommended to be small.

    Additional metadata, as specified by the licence type, is also stored.
    '''

    licence_type = models.ForeignKey(
        'LicenceType',
        on_delete=models.PROTECT,
        db_column='licence_type_id',
        verbose_name=_('licence type'),
        help_text=_('Type of licence used'),
        blank=False,
        null=False)

    document = models.FileField(
        upload_to='documents/licences/',
        db_column='document',
        verbose_name=_('document'),
        help_text=_('Legal document of licence agreement'),
        blank=True)

    metadata = models.JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated with licence'),
        blank=True,
        null=True)

    is_active = models.BooleanField(
        editable=False,
        db_column='is_active',
        verbose_name=_('is active'),
        help_text=_('Licence is still active'),
        default=False,
        blank=True,
        null=False)

    class Meta:
        verbose_name = _('Licence')

        verbose_name_plural = _('Licences')

        ordering = ['-created_on']

    def __str__(self):
        msg = _('{type} - {date}').format(
            type=str(self.licence_type),
            date=self.created_on.strftime("%d/%m/%Y"))
        return msg

    def clean(self):
        super().clean()

        # Update licence status if the active period is over
        self.update_is_active()

        # Check that metadata is valid
        self.clean_metadata()

    def clean_metadata(self):
        try:
            # pylint: disable=no-member
            self.licence_type.validate_metadata(self.metadata)

        except ValidationError as error:
            raise ValidationError({'metadata': error}) from error

    def update_is_active(self):
        """Modify active state if licence is outdated"""
        if self.created_on is None:
            # When licence is beign created the attribute created_on is null
            self.is_active = True
            return

        # pylint: disable=no-member
        duration_in_years = self.licence_type.years_valid_for
        current_time_offset = timezone.now() - self.created_on
        year_offset = current_time_offset.days / 365

        self.is_active = year_offset <= duration_in_years