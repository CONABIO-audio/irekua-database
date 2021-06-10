# Generated by Django 3.1.2 on 2020-10-20 17:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("irekua_database", "0014_auto_20201017_2008"),
        ("irekua_schemas", "0002_auto_20201018_2158"),
        ("irekua_types", "0005_auto_20201019_1402"),
        ("irekua_collections", "0002_migrate_to_foreing_key_schemas"),
    ]

    operations = [
        migrations.RenameModel(
            "CollectionItemType",
            "CollectionTypeItemType",
        ),
        migrations.RenameModel(
            "CollectionDeviceType",
            "CollectionTypeDeviceType",
        ),
        migrations.RenameModel(
            "CollectionRole",
            "CollectionTypeRole",
        ),
        migrations.AlterModelOptions(
            name="collectiontypedevicetype",
            options={
                "verbose_name": "Collection Type Device Type",
                "verbose_name_plural": "Collection Type Device Types",
            },
        ),
        migrations.AlterModelOptions(
            name="collectiontypeitemtype",
            options={
                "verbose_name": "Collection Type Item Type",
                "verbose_name_plural": "Collection Type Item Types",
            },
        ),
        migrations.AlterModelOptions(
            name="collectiontyperole",
            options={
                "verbose_name": "Collection Type Role",
                "verbose_name_plural": "Collection Type Roles",
            },
        ),
        migrations.AlterField(
            model_name="collectiontypedevicetype",
            name="metadata_schema",
            field=models.ForeignKey(
                blank=True,
                db_column="metadata_schema_id",
                help_text="JSON Schema for collection-specific metadata",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="collectiontypedevicetype_metadata_schema",
                to="irekua_schemas.schema",
                verbose_name="metadata schema",
            ),
        ),
        migrations.AlterField(
            model_name="collectiontypeitemtype",
            name="metadata_schema",
            field=models.ForeignKey(
                blank=True,
                db_column="metadata_schema_id",
                help_text="JSON Schema for collection-specific metadata",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="collectiontypeitemtype_metadata_schema",
                to="irekua_schemas.schema",
                verbose_name="metadata schema",
            ),
        ),
        migrations.AlterField(
            model_name="collectiontyperole",
            name="metadata_schema",
            field=models.ForeignKey(
                blank=True,
                db_column="metadata_schema_id",
                help_text="JSON Schema for collection-specific metadata",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="collectiontyperole_metadata_schema",
                to="irekua_schemas.schema",
                verbose_name="metadata schema",
            ),
        ),
    ]