from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from irekua_database.base import IrekuaModelBaseUser
from irekua_collections.models import Collection
from irekua_terms.models import Term


class Organism(IrekuaModelBaseUser):
    collection = models.ForeignKey(
        Collection,
        db_column="collection_id",
        verbose_name=_("collection"),
        help_text=_("Collection to which this organism belongs"),
        on_delete=models.PROTECT,
        blank=False,
        null=False,
    )

    organism_type = models.ForeignKey(
        "OrganismType",
        db_column="organism_type_id",
        verbose_name=_("organism type"),
        help_text=_("Type of organism"),
        on_delete=models.PROTECT,
        blank=False,
        null=False,
    )

    name = models.CharField(
        max_length=64,
        db_column="name",
        verbose_name=_("name"),
        unique=True,
        help_text=_(
            "A textual name or label assigned to an Organism instance"
        ),
        blank=True,
        null=True,
    )

    remarks = models.TextField(
        db_column="remarks",
        verbose_name=_("remarks"),
        help_text=_("Comments or notes about the Organism instance"),
        blank=True,
    )

    identification_info = models.JSONField(
        db_column="identification_info",
        verbose_name=_("identification info"),
        help_text=_("Organism identification information."),
        blank=True,
        null=True,
    )

    metadata = models.JSONField(
        db_column="metadata",
        verbose_name=_("metadata"),
        help_text=_("Additional metadata associated to organism"),
        blank=True,
        null=True,
    )

    collection_metadata = models.JSONField(
        db_column="collection_metadata",
        verbose_name=_("collection metadata"),
        help_text=_(
            "Additional metadata associated to organism in collection"
        ),
        blank=True,
        null=True,
    )

    labels = models.ManyToManyField(
        Term,
        verbose_name=_("labels"),
        help_text=_("Description of the organism"),
        blank=True,
    )

    class Meta:
        verbose_name = _("Organism")
        verbose_name_plural = _("Organisms")
        ordering = ["-created_on"]

    def __str__(self):
        if self.name:
            return str(self.name)

        msg = _("Organism %(id)s")
        params = dict(id=self.id)
        return msg % params

    def clean(self):
        super().clean()

        #  Check if collection has been configured to use organisms
        organism_config = self.clean_organism_config()

        # Check if collection type allows organisms
        self.clean_collection_type(organism_config)

        # Check that metadata is valid for organism type
        self.clean_metadata()

        # Check that identification info is valid for organism type
        self.clean_identification_info()

        #  No futher validation is required if organism types are not
        # restricted
        if not organism_config.restrict_organism_types:
            return

        # Check organism type is allowed in collections of this type
        organism_type_config = self.clean_organism_type(organism_config)

        # Check that additional collection metadata is valid for organism type
        self.clean_collection_metadata(organism_type_config)

    def clean_organism_config(self):
        # pylint: disable=no-member
        collection_type = self.collection.collection_type

        try:
            return collection_type.collectiontypeorganismconfig

        except ObjectDoesNotExist as error:
            msg = _(
                "Collections of type %(collection_type)s do not allow "
                "organisms."
            )
            params = dict(collection_type=collection_type)
            raise ValidationError({"collection": msg % params}) from error

    # pylint: disable=no-self-use
    def clean_collection_type(self, organism_config):
        if not organism_config.use_organisms:
            msg = _("This collection does not allow organisms")
            raise ValidationError(msg)

    def clean_organism_type(self, organism_config):
        try:
            return organism_config.get_organism_type(self.organism_type)

        except ObjectDoesNotExist as error:
            raise ValidationError({"organism_type": error}) from error

    def clean_identification_info(self):
        try:
            # pylint: disable=no-member
            self.organism_type.validate_id_info(self.identification_info)

        except ValidationError as error:
            raise ValueError({"identification_info": error}) from error

    def clean_metadata(self):
        try:
            # pylint: disable=no-member
            self.organism_type.validate_metadata(self.metadata)

        except ValidationError as error:
            raise ValidationError({"metadata": error}) from error

    def clean_collection_metadata(self, organism_type_config):
        try:
            organism_type_config.validate_metadata(self.collection_metadata)

        except ValidationError as error:
            raise ValidationError({"collection_metadata": error}) from error
