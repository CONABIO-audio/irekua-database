# Generated by Django 3.1 on 2020-10-13 00:43

from django.conf import settings
import django.contrib.gis.db.models.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import irekua_database.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("irekua_types", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name="Locality",
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
                            "name",
                            models.CharField(
                                db_column="name",
                                help_text="Name of locality",
                                max_length=128,
                            ),
                        ),
                        (
                            "description",
                            models.TextField(
                                blank=True,
                                db_column="description",
                                help_text="Description of the locality",
                                verbose_name="description",
                            ),
                        ),
                        (
                            "geometry",
                            django.contrib.gis.db.models.fields.MultiPolygonField(
                                blank=True,
                                db_column="geometry",
                                help_text="Geometry of locality",
                                srid=4326,
                                verbose_name="geometry",
                            ),
                        ),
                        (
                            "metadata",
                            models.JSONField(
                                blank=True,
                                db_column="metadata",
                                default=irekua_database.utils.empty_JSON,
                                help_text="Metadata associated to locality",
                                null=True,
                                verbose_name="metadata",
                            ),
                        ),
                        (
                            "is_part_of",
                            models.ManyToManyField(
                                blank=True, to="irekua_geo.Locality"
                            ),
                        ),
                        (
                            "locality_type",
                            models.ForeignKey(
                                db_column="locality_type_id",
                                help_text="Type of locality",
                                on_delete=django.db.models.deletion.PROTECT,
                                to="irekua_types.localitytype",
                                verbose_name="locality type",
                            ),
                        ),
                    ],
                    options={
                        "verbose_name": "Locality",
                        "verbose_name_plural": "Localities",
                        "ordering": ["-name"],
                    },
                ),
                migrations.CreateModel(
                    name="Site",
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
                                help_text="Name of site (visible only to owner)",
                                max_length=128,
                                null=True,
                                verbose_name="name",
                            ),
                        ),
                        (
                            "geo_ref",
                            django.contrib.gis.db.models.fields.PointField(
                                blank=True,
                                db_column="geo_ref",
                                help_text="Georeference of site as Geometry",
                                srid=4326,
                                verbose_name="geo ref",
                            ),
                        ),
                        (
                            "latitude",
                            models.FloatField(
                                blank=True,
                                db_column="latitude",
                                help_text="Latitude of site (in decimal degrees)",
                                validators=[
                                    django.core.validators.MinValueValidator(
                                        -90
                                    ),
                                    django.core.validators.MaxValueValidator(
                                        90
                                    ),
                                ],
                                verbose_name="latitude",
                            ),
                        ),
                        (
                            "longitude",
                            models.FloatField(
                                blank=True,
                                db_column="longitude",
                                help_text="Longitude of site (in decimal degrees)",
                                validators=[
                                    django.core.validators.MinValueValidator(
                                        -180
                                    ),
                                    django.core.validators.MaxValueValidator(
                                        180
                                    ),
                                ],
                                verbose_name="longitude",
                            ),
                        ),
                        (
                            "altitude",
                            models.FloatField(
                                blank=True,
                                db_column="altitude",
                                help_text="Altitude of site (in meters)",
                                null=True,
                                verbose_name="altitude",
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
                                related_name="site_created_by",
                                to=settings.AUTH_USER_MODEL,
                                verbose_name="creator",
                            ),
                        ),
                        (
                            "locality",
                            models.ForeignKey(
                                blank=True,
                                db_column="locality_id",
                                help_text="Name of locality in which the site is located",
                                null=True,
                                on_delete=django.db.models.deletion.PROTECT,
                                to="irekua_geo.locality",
                                verbose_name="locality",
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
                                related_name="site_modified_by",
                                to=settings.AUTH_USER_MODEL,
                                verbose_name="modified by",
                            ),
                        ),
                    ],
                    options={
                        "verbose_name": "Site",
                        "verbose_name_plural": "Sites",
                        "ordering": ["-created_on"],
                    },
                ),
                migrations.CreateModel(
                    name="SiteDescriptor",
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
                            "value",
                            models.CharField(
                                db_column="value",
                                help_text="Value of descriptor",
                                max_length=128,
                                verbose_name="value",
                            ),
                        ),
                        (
                            "description",
                            models.TextField(
                                blank=True,
                                db_column="description",
                                help_text="Description of term",
                                verbose_name="description",
                            ),
                        ),
                        (
                            "metadata",
                            models.JSONField(
                                blank=True,
                                db_column="metadata",
                                default=irekua_database.utils.empty_JSON,
                                help_text="Metadata associated to term",
                                null=True,
                                verbose_name="metadata",
                            ),
                        ),
                        (
                            "descriptor_type",
                            models.ForeignKey(
                                db_column="descriptor_type",
                                help_text="Type of site descriptor",
                                on_delete=django.db.models.deletion.CASCADE,
                                to="irekua_types.sitedescriptortype",
                                verbose_name="descriptor type",
                            ),
                        ),
                    ],
                    options={
                        "verbose_name": "Site Descriptor",
                        "verbose_name_plural": "Site Descriptors",
                        "ordering": ["descriptor_type", "value"],
                        "unique_together": {("descriptor_type", "value")},
                    },
                ),
            ],
            database_operations=[],
        ),
    ]
