from django.db import models
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBaseUser


class SamplingEvent(IrekuaModelBaseUser):
    sampling_event_type = models.ForeignKey(
        "SamplingEventType",
        on_delete=models.PROTECT,
        db_column="sampling_event_type",
        verbose_name=_("sampling event type"),
        help_text=_("Type of sampling event"),
        blank=False,
        null=False,
    )

    collection_site = models.ForeignKey(
        "CollectionSite",
        db_column="collection_site_id",
        verbose_name=_("collection site"),
        help_text=_("Reference to site at which sampling took place"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    commentaries = models.TextField(
        db_column="commentaries",
        verbose_name=_("commentaries"),
        help_text=_("Sampling event commentaries"),
        blank=True,
    )

    metadata = models.JSONField(
        db_column="metadata",
        verbose_name=_("metadata"),
        help_text=_("Metadata associated to sampling event"),
        blank=True,
        null=True,
    )

    collection_metadata = models.JSONField(
        db_column="collection_metadata",
        verbose_name=_("collection metadata"),
        help_text=_("Additional metadata associated to sampling event in collection"),
        blank=True,
        null=True,
    )

    started_on = models.DateTimeField(
        db_column="started_on",
        verbose_name=_("started on"),
        help_text=_("Date at which sampling begun"),
        blank=True,
        null=True,
    )

    ended_on = models.DateTimeField(
        db_column="ended_on",
        verbose_name=_("ended on"),
        help_text=_("Date at which sampling stoped"),
        blank=True,
        null=True,
    )

    collection = models.ForeignKey(
        "Collection",
        on_delete=models.PROTECT,
        db_column="collection_id",
        verbose_name=_("collection"),
        help_text=_("Collection to which sampling event belongs"),
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = _("Sampling Event")

        verbose_name_plural = _("Sampling Events")

        ordering = ["-created_on"]

    def __str__(self):
        msg = _("%(site)s - %(date)s")
        params = dict(
            site=str(self.collection_site), date=self.started_on.strftime("%m/%Y")
        )
        return msg % params

    def clean(self):
        super().clean()

        # Check if collection site and collection are compatible
        self.clean_equal_collections()

        # Check that starting date is earlier than ending date
        self.clean_valid_dates()

        # Check that site type and sampling event type are compatible
        self.clean_compatible_site_and_sampling_event_types()

        # Check metadata is valid for sampling event type
        self.clean_valid_metadata()

        #  Check that deployment dates do not fall outside the sampling event's
        # date range
        self.clean_consistent_deployment_dates()

        # Check that any registered items do fall outside the the sampling event's
        # date range
        self.clean_consistent_item_dates()

        # pylint: disable=no-member
        collection_type = self.collection.collection_type

        # If collection type does not restrict sampling event types
        # no further validation is required
        if not collection_type.restrict_sampling_event_types:
            return

        # Check that this sampling event type is registered for this collection
        # type
        sampling_event_config = self.clean_allowed_sampling_event_type(collection_type)

        # Check if additional collection metadata is valid for this sampling event type
        self.clean_valid_collection_metadata(sampling_event_config)

    def clean_equal_collections(self):
        #  pylint: disable=no-member
        if self.collection != self.collection_site.collection:
            msg = _("Site does not belong to the declared collection")
            raise ValidationError({"collection_site": msg})

    def clean_valid_dates(self):
        if self.started_on > self.ended_on:
            msg = _("Starting date cannot be greater than ending date")
            raise ValidationError({"started_on": msg})

    def clean_compatible_site_and_sampling_event_types(self):
        #  pylint: disable=no-member
        site_type = self.collection_site.site_type

        try:
            self.sampling_event_type.validate_site_type(site_type)

        except ValidationError as error:
            msg = _(
                "A sampling event of type %(sampling_event_type)s cannot "
                "be declared in a site of type %(site_type)s"
            )
            params = dict(
                sampling_event_type=self.sampling_event_type, site_type=site_type
            )
            raise ValidationError({"collection_site": msg % params}) from error

    def clean_valid_metadata(self):
        try:
            # pylint: disable=no-member
            self.sampling_event_type.validate_metadata(self.metadata)

        except ValidationError as error:
            raise ValidationError({"metadata": error}) from error

    def clean_allowed_sampling_event_type(self, collection_type):
        try:
            return collection_type.get_sampling_event_type(self.sampling_event_type)

        except ObjectDoesNotExist as error:
            msg = _(
                "Sampling events of type %(sampling_event_type)s are not allowed in "
                "collections of type %(collection_type)s"
            )
            params = dict(
                sampling_event_type=self.sampling_event_type,
                collection_type=collection_type,
            )
            raise ValidationError({"sampling_event_type": msg % params}) from error

    def clean_valid_collection_metadata(self, sampling_event_config):
        try:
            sampling_event_config.validate_metadata(self.collection_metadata)

        except ValidationError as error:
            raise ValidationError({"collection_metadata": str(error)}) from error

    def clean_consistent_deployment_dates(self):
        if self.id is None:
            # Exit early if sampling event is being created
            return

        if (self.started_on is None) and (self.ended_on is None):
            return

        queryset = self.deployment_set.all()

        if self.started_on is not None:
            if queryset.filter(
                models.Q(recovered_on__lt=self.started_on)
                | models.Q(deployed_on__lt=self.started_on)
            ).exists():
                msg = _(
                    "Registered deployments occur before the sampling event's "
                    "declared date range"
                )
                raise ValidationError({"started_on": msg})

        if self.ended_on is not None:
            if queryset.filter(
                models.Q(recovered_on__gt=self.ended_on)
                | models.Q(deployed_on__gt=self.ended_on)
            ).exists():
                msg = _(
                    "Registered deployments occur after the sampling event's "
                    "declared date range"
                )
                raise ValidationError({"ended_on": msg})

    def clean_consistent_item_dates(self):
        if self.id is None:
            # Exit early if sampling event is being created
            return

        if (self.started_on is None) and (self.ended_on is None):
            return

        #  Check on all sampling event items but exclude deployment items
        # since their dates are validated when associated to the deployment.
        queryset = self.samplingeventitem_set.filter(deploymentitem__isnull=True)

        if self.started_on is not None:
            if queryset.filter(captured_on__lt=self.started_on).exists():
                msg = _(
                    "There are items associated to this sampling event that "
                    "where captured before the start of the sampling event."
                )
                raise ValidationError({"started_on": msg})

        if self.ended_on is not None:
            if queryset.filter(captured_on__gt=self.ended_on).exists():
                msg = _(
                    "There are items associated to this sampling event that "
                    "where captured after the end of the sampling event."
                )
                raise ValidationError({"ended_on": msg})

    def validate_date(self, date_info):
        if self.started_on is not None:
            if date_info < self.started_on:
                msg = _("Date provided is earlier that the sampling event start")
                raise ValidationError(msg)

        if self.ended_on is not None:
            if date_info > self.ended_on:
                msg = _("Date provided is later that the sampling event end")
                raise ValidationError(msg)

    @property
    def items(self):
        from irekua_collections.models import SamplingEventItem

        return SamplingEventItem.objects.filter(sampling_event=self)
