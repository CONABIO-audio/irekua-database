# Generated by Django 3.1 on 2020-10-13 13:52
from django.db import migrations, models
import django.db.models.deletion


def create_schemas(apps, schema_editor):
    Schema = apps.get_model("irekua_schemas", "Schema")
    TermType = apps.get_model("irekua_terms", "TermType")
    EntailmentType = apps.get_model("irekua_terms", "EntailmentType")

    schemas = {}

    def get_schema(metadata_schema):
        title = metadata_schema.get("title", None)

        if title is None:
            return None

        if title in schemas:
            return schemas[title]

        schema = Schema(
            name=title,
            description=metadata_schema.get("description", ""),
            schema=metadata_schema,
        )
        schema.save()

        schemas[title] = schema
        return schema

    for term_type in TermType.objects.all():
        metadata_schema = term_type.metadata_schema
        synonym_metadata_schema = term_type.synonym_metadata_schema
        term_type.metadata_schema_tmp = get_schema(metadata_schema)
        term_type.synonym_metadata_schema_tmp = get_schema(
            synonym_metadata_schema
        )
        term_type.save()

    for entailment_type in EntailmentType.objects.all():
        metadata_schema = entailment_type.metadata_schema
        entailment_type.metadata_schema_tmp = get_schema(metadata_schema)
        entailment_type.save()


class Migration(migrations.Migration):

    dependencies = [
        ("irekua_schemas", "0001_initial"),
        ("irekua_terms", "0001_initial"),
        ("irekua_database", "0004_move_terms"),
    ]

    operations = [
        migrations.AddField(
            model_name="entailmenttype",
            name="metadata_schema_tmp",
            field=models.ForeignKey(
                blank=True,
                db_column="metadata_schema_id",
                help_text="JSON Schema for metadata of entailment info",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="irekua_schemas.schema",
                verbose_name="metadata schema",
            ),
        ),
        migrations.AddField(
            model_name="termtype",
            name="metadata_schema_tmp",
            field=models.ForeignKey(
                blank=True,
                db_column="metadata_schema_id",
                help_text="JSON Schema for metadata of term info",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="term_metadata_schema",
                to="irekua_schemas.schema",
                verbose_name="metadata schema",
            ),
        ),
        migrations.AddField(
            model_name="termtype",
            name="synonym_metadata_schema_tmp",
            field=models.ForeignKey(
                blank=True,
                db_column="synonym_metadata_schema_id",
                help_text="JSON Schema for metadata of synonym info",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="synonym_metadata_schema",
                to="irekua_schemas.schema",
                verbose_name="synonym metadata schema",
            ),
        ),
        migrations.RunPython(
            create_schemas,
        ),
        migrations.RemoveField(
            model_name="entailmenttype",
            name="metadata_schema",
        ),
        migrations.RemoveField(
            model_name="termtype",
            name="metadata_schema",
        ),
        migrations.RemoveField(
            model_name="termtype",
            name="synonym_metadata_schema",
        ),
        migrations.RenameField(
            model_name="termtype",
            old_name="metadata_schema_tmp",
            new_name="metadata_schema",
        ),
        migrations.RenameField(
            model_name="termtype",
            old_name="synonym_metadata_schema_tmp",
            new_name="synonym_metadata_schema",
        ),
        migrations.RenameField(
            model_name="entailmenttype",
            old_name="metadata_schema_tmp",
            new_name="metadata_schema",
        ),
    ]
