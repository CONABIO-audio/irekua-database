# Generated by Django 3.1.2 on 2020-10-21 22:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import irekua_database.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("irekua_terms", "0005_auto_20201018_1704"),
        (
            "irekua_collections",
            "0009_relocate_deployment_and_sampling_event_types",
        ),
        ("irekua_items", "0003_auto_20201019_1658"),
        ("irekua_types", "0006_relocate_deployment_and_sampling_event_types"),
    ]

    operations = [
        migrations.CreateModel(
            name="CollectionTypeOrganismCaptureType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_column="created_on",
                        help_text="Date of creation",
                        verbose_name="created on",
                    ),
                ),
                (
                    "modified_on",
                    models.DateTimeField(
                        auto_now=True,
                        db_column="modified_on",
                        help_text="Date of last modification",
                        verbose_name="modified on",
                    ),
                ),
                (
                    "metadata_schema",
                    models.JSONField(
                        blank=True,
                        db_column="metadata_schema",
                        default=irekua_database.utils.simple_JSON_schema,
                        help_text="JSON Schema for additional metadata of this type of organism capture in this type of collections.",
                        validators=[
                            irekua_database.utils.validate_JSON_schema
                        ],
                        verbose_name="additional metadata schema",
                    ),
                ),
            ],
            options={
                "verbose_name": "Collection Type Organism Capture Type",
                "verbose_name_plural": "Collection Type Organism Capture Types",
                "ordering": ["-created_on"],
            },
        ),
        migrations.CreateModel(
            name="CollectionTypeOrganismConfig",
            fields=[
                (
                    "created_on",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_column="created_on",
                        help_text="Date of creation",
                        verbose_name="created on",
                    ),
                ),
                (
                    "modified_on",
                    models.DateTimeField(
                        auto_now=True,
                        db_column="modified_on",
                        help_text="Date of last modification",
                        verbose_name="modified on",
                    ),
                ),
                (
                    "collection_type",
                    models.OneToOneField(
                        help_text="Collection Type to be configured.",
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="irekua_collections.collectiontype",
                    ),
                ),
                (
                    "use_organisms",
                    models.BooleanField(
                        db_column="use_organisms",
                        default=False,
                        help_text="Boolean flag indicating whether organisms are to be used in this collection type.",
                        verbose_name="use organisms",
                    ),
                ),
            ],
            options={
                "verbose_name": "Collection Type Organism Configuration",
                "verbose_name_plural": "Collection Type Organism Configurations",
                "ordering": ["-created_on"],
            },
        ),
        migrations.CreateModel(
            name="Organism",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_column="created_on",
                        help_text="Date of creation",
                        verbose_name="created on",
                    ),
                ),
                (
                    "modified_on",
                    models.DateTimeField(
                        auto_now=True,
                        db_column="modified_on",
                        help_text="Date of last modification",
                        verbose_name="modified on",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        db_column="name",
                        help_text="A textual name or label assigned to an Organism instance",
                        max_length=64,
                        null=True,
                        unique=True,
                        verbose_name="name",
                    ),
                ),
                (
                    "remarks",
                    models.TextField(
                        blank=True,
                        db_column="remarks",
                        help_text="Comments or notes about the Organism instance",
                        verbose_name="remarks",
                    ),
                ),
                (
                    "identification_info",
                    models.JSONField(
                        blank=True,
                        db_column="identification_info",
                        default=irekua_database.utils.empty_JSON,
                        help_text="Organism identification information.",
                        verbose_name="identification info",
                    ),
                ),
                (
                    "additional_metadata",
                    models.JSONField(
                        blank=True,
                        db_column="additional_metadata",
                        default=irekua_database.utils.empty_JSON,
                        help_text="Additional organism metadata",
                        verbose_name="additional metadata",
                    ),
                ),
                (
                    "collection",
                    models.ForeignKey(
                        db_column="collection_id",
                        help_text="Collection to which this organism belongs",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="irekua_collections.collection",
                        verbose_name="collection",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        db_column="creator_id",
                        help_text="Creator of object",
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="organism_created_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="creator",
                    ),
                ),
                (
                    "items",
                    models.ManyToManyField(
                        help_text="Items associated to this organism",
                        to="irekua_items.Item",
                        verbose_name="items",
                    ),
                ),
                (
                    "labels",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Description of the organism",
                        to="irekua_terms.Term",
                        verbose_name="labels",
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        db_column="modified_by",
                        editable=False,
                        help_text="User who made modifications last",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="organism_modified_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="modified by",
                    ),
                ),
            ],
            options={
                "verbose_name": "Organism",
                "verbose_name_plural": "Organisms",
                "ordering": ["-created_on"],
            },
        ),
        migrations.CreateModel(
            name="OrganismType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_column="created_on",
                        help_text="Date of creation",
                        verbose_name="created on",
                    ),
                ),
                (
                    "modified_on",
                    models.DateTimeField(
                        auto_now=True,
                        db_column="modified_on",
                        help_text="Date of last modification",
                        verbose_name="modified on",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_column="name",
                        help_text="Name of organism type",
                        max_length=64,
                        unique=True,
                        verbose_name="name",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        db_column="description",
                        help_text="Description of organism type",
                        verbose_name="description",
                    ),
                ),
                (
                    "icon",
                    models.ImageField(
                        blank=True,
                        db_column="icon",
                        help_text="Organism type icon",
                        null=True,
                        upload_to="images/organism_types/",
                        verbose_name="icon",
                    ),
                ),
                (
                    "identification_info_schema",
                    models.JSONField(
                        blank=True,
                        db_column="identification_info_schema",
                        default=irekua_database.utils.simple_JSON_schema,
                        help_text="JSON Schema for identification information.",
                        validators=[
                            irekua_database.utils.validate_JSON_schema
                        ],
                        verbose_name="identification information schema",
                    ),
                ),
                (
                    "is_multi_organism",
                    models.BooleanField(
                        db_column="is_multi_organism",
                        default=False,
                        help_text="Boolean flag that indicates whether this organismmay be composed by multiple organisms.",
                        verbose_name="is multi organism",
                    ),
                ),
                (
                    "term_types",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Valid term types to describe the organism",
                        to="irekua_terms.TermType",
                        verbose_name="term types",
                    ),
                ),
            ],
            options={
                "verbose_name": "Organism Type",
                "verbose_name_plural": "Organism Types",
                "ordering": ["-created_on"],
            },
        ),
        migrations.CreateModel(
            name="OrganismCaptureType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_column="created_on",
                        help_text="Date of creation",
                        verbose_name="created on",
                    ),
                ),
                (
                    "modified_on",
                    models.DateTimeField(
                        auto_now=True,
                        db_column="modified_on",
                        help_text="Date of last modification",
                        verbose_name="modified on",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_column="name",
                        help_text="Name of organism capture type",
                        max_length=64,
                        unique=True,
                        verbose_name="name",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        db_column="description",
                        help_text="Description of organism capture type",
                        verbose_name="description",
                    ),
                ),
                (
                    "icon",
                    models.ImageField(
                        blank=True,
                        db_column="icon",
                        help_text="Organism capture type icon",
                        null=True,
                        upload_to="images/organism_types/",
                        verbose_name="icon",
                    ),
                ),
                (
                    "device_type",
                    models.ForeignKey(
                        db_column="device_type_id",
                        help_text="Device type used for capture",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="irekua_types.devicetype",
                        verbose_name="device type",
                    ),
                ),
                (
                    "organism_type",
                    models.ForeignKey(
                        db_column="organism_type_id",
                        help_text="Organism type being captured",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="irekua_organisms.organismtype",
                        verbose_name="organism type",
                    ),
                ),
                (
                    "term_types",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Valid term types to describe the organism capture",
                        to="irekua_terms.TermType",
                        verbose_name="term types",
                    ),
                ),
            ],
            options={
                "verbose_name": "Organism Capture Type",
                "verbose_name_plural": "Organism Capture Types",
                "ordering": ["-created_on"],
            },
        ),
        migrations.CreateModel(
            name="OrganismCapture",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_column="created_on",
                        help_text="Date of creation",
                        verbose_name="created on",
                    ),
                ),
                (
                    "modified_on",
                    models.DateTimeField(
                        auto_now=True,
                        db_column="modified_on",
                        help_text="Date of last modification",
                        verbose_name="modified on",
                    ),
                ),
                (
                    "additional_metadata",
                    models.JSONField(
                        blank=True,
                        db_column="additional_metadata",
                        default=irekua_database.utils.empty_JSON,
                        help_text="Additional organism metadata",
                        verbose_name="additional metadata",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        db_column="creator_id",
                        help_text="Creator of object",
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="organismcapture_created_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="creator",
                    ),
                ),
                (
                    "items",
                    models.ManyToManyField(
                        help_text="Items associated to this organism",
                        to="irekua_items.Item",
                        verbose_name="items",
                    ),
                ),
                (
                    "labels",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Description of the organism capture",
                        to="irekua_terms.Term",
                        verbose_name="labels",
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        db_column="modified_by",
                        editable=False,
                        help_text="User who made modifications last",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="organismcapture_modified_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="modified by",
                    ),
                ),
                (
                    "organism",
                    models.ForeignKey(
                        db_column="organism_id",
                        help_text="Captured organism",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="irekua_organisms.organism",
                        verbose_name="organism",
                    ),
                ),
                (
                    "organism_capture_type",
                    models.ForeignKey(
                        db_column="organism_capture_type_id",
                        help_text="Capture type",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="irekua_organisms.organismcapturetype",
                        verbose_name="organism capture type",
                    ),
                ),
                (
                    "sampling_event_device",
                    models.ForeignKey(
                        db_column="sampling_event_device_id",
                        help_text="Device used to capture this organism",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="irekua_collections.deployment",
                        verbose_name="sampling event device",
                    ),
                ),
            ],
            options={
                "verbose_name": "Organism Capture",
                "verbose_name_plural": "Organism Captures",
                "ordering": ["-created_on"],
            },
        ),
        migrations.AddField(
            model_name="organism",
            name="organism_type",
            field=models.ForeignKey(
                db_column="organism_type_id",
                help_text="Type of organism",
                on_delete=django.db.models.deletion.PROTECT,
                to="irekua_organisms.organismtype",
                verbose_name="organism type",
            ),
        ),
        migrations.CreateModel(
            name="CollectionTypeOrganismType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_column="created_on",
                        help_text="Date of creation",
                        verbose_name="created on",
                    ),
                ),
                (
                    "modified_on",
                    models.DateTimeField(
                        auto_now=True,
                        db_column="modified_on",
                        help_text="Date of last modification",
                        verbose_name="modified on",
                    ),
                ),
                (
                    "metadata_schema",
                    models.JSONField(
                        blank=True,
                        db_column="metadata_schema",
                        default=irekua_database.utils.simple_JSON_schema,
                        help_text="JSON Schema for additional metadata of this type of organisms in this type of collections.",
                        validators=[
                            irekua_database.utils.validate_JSON_schema
                        ],
                        verbose_name="additional metadata schema",
                    ),
                ),
                (
                    "collection_type_organism_config",
                    models.ForeignKey(
                        db_column="collection_type_organism_config_id",
                        help_text="Collection type organism configuration",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="irekua_organisms.collectiontypeorganismconfig",
                        verbose_name="collection type organism config",
                    ),
                ),
                (
                    "organism_type",
                    models.ForeignKey(
                        db_column="organism_type_id",
                        help_text="Organism type to be registered to the collection type",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="irekua_organisms.organismtype",
                        verbose_name="organism type",
                    ),
                ),
            ],
            options={
                "verbose_name": "Collection Type Organism Type",
                "verbose_name_plural": "Collection Type Organism Types",
                "ordering": ["-created_on"],
                "unique_together": {
                    ("collection_type_organism_config", "organism_type")
                },
            },
        ),
        migrations.AddField(
            model_name="collectiontypeorganismconfig",
            name="organism_capture_types",
            field=models.ManyToManyField(
                blank=True,
                help_text="Types of organism captures that can be registered into collections of this type.",
                through="irekua_organisms.CollectionTypeOrganismCaptureType",
                to="irekua_organisms.OrganismCaptureType",
                verbose_name="organism capture types",
            ),
        ),
        migrations.AddField(
            model_name="collectiontypeorganismconfig",
            name="organism_types",
            field=models.ManyToManyField(
                blank=True,
                help_text="Types of organisms that can be registered into collections of this type.",
                through="irekua_organisms.CollectionTypeOrganismType",
                to="irekua_organisms.OrganismType",
                verbose_name="organism types",
            ),
        ),
        migrations.AddField(
            model_name="collectiontypeorganismcapturetype",
            name="collection_type_organism_config",
            field=models.ForeignKey(
                db_column="collection_type_organism_config_id",
                help_text="Collection type organism configuration",
                on_delete=django.db.models.deletion.CASCADE,
                to="irekua_organisms.collectiontypeorganismconfig",
                verbose_name="collection type organism config",
            ),
        ),
        migrations.AddField(
            model_name="collectiontypeorganismcapturetype",
            name="organism_capture_type",
            field=models.ForeignKey(
                db_column="organism_capture_type_id",
                help_text="Organism capture type to be registered to the collection type",
                on_delete=django.db.models.deletion.PROTECT,
                to="irekua_organisms.organismcapturetype",
                verbose_name="organism capture type",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="collectiontypeorganismcapturetype",
            unique_together={
                ("collection_type_organism_config", "organism_capture_type")
            },
        ),
    ]
