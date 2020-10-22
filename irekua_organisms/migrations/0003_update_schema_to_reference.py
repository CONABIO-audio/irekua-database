# Generated by Django 3.1.2 on 2020-10-22 01:45
import json
from django.db import migrations, models
import django.db.models.deletion


def move_json_schema_to_foreign_key(model_name, field):
    def python_migration(apps, schema_editor):
        Schema = apps.get_model('irekua_schemas', 'Schema')
        Model = apps.get_model('irekua_organisms', model_name)

        schemas = {}

        def get_schema_object_from_schema(schema):
            if isinstance(schema, str):
                schema = json.loads(schema)

            title = schema.get('title', None)
            description = schema.get('description', '')

            if title is None:
                return None

            if title in schemas:
                return schemas[title]

            schema_object, _ = Schema.objects.get_or_create(
                name=title,
                defaults={
                    'description': description,
                    'schema': schema
                }
            )

            schemas[title] = schema_object
            return schema_object

        for obj in Model.objects.all():
            schema = getattr(obj, field, None)

            if schema is None:
                continue

            schema_object = get_schema_object_from_schema(schema)
            setattr(obj, f'{field}_tmp', schema_object)
            obj.save()

    return python_migration


class Migration(migrations.Migration):

    dependencies = [
        ('irekua_schemas', '0002_auto_20201018_2158'),
        ('irekua_organisms', '0002_update_device_type_models_reference'),
    ]

    operations = [
        migrations.AddField(
            model_name='organismcapturetype',
            name='metadata_schema',
            field=models.ForeignKey(blank=True, db_column='metadata_schema_id', help_text='JSON Schema for additional metadata', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='organismcapturetype_metadata_schema', to='irekua_schemas.schema', verbose_name='metadata schema'),
        ),
        migrations.AddField(
            model_name='organismtype',
            name='metadata_schema',
            field=models.ForeignKey(blank=True, db_column='metadata_schema_id', help_text='JSON Schema for additional metadata', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='organismtype_metadata_schema', to='irekua_schemas.schema', verbose_name='metadata schema'),
        ),
        migrations.AddField(
            model_name='collectiontypeorganismcapturetype',
            name='metadata_schema_tmp',
            field=models.ForeignKey(blank=True, db_column='metadata_schema_id', help_text='JSON Schema for collection-specific metadata', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='collectiontypeorganismcapturetype_metadata_schema', to='irekua_schemas.schema', verbose_name='metadata schema'),
        ),
        migrations.RunPython(
            move_json_schema_to_foreign_key('CollectionTypeOrganismCaptureType', 'metadata_schema')
        ),
        migrations.RemoveField(
            model_name='collectiontypeorganismcapturetype',
            name='metadata_schema',
        ),
        migrations.RenameField(
            model_name='collectiontypeorganismcapturetype',
            old_name='metadata_schema_tmp',
            new_name='metadata_schema',
        ),
        migrations.AddField(
            model_name='collectiontypeorganismtype',
            name='metadata_schema_tmp',
            field=models.ForeignKey(blank=True, db_column='metadata_schema_id', help_text='JSON Schema for collection-specific metadata', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='collectiontypeorganismtype_metadata_schema', to='irekua_schemas.schema', verbose_name='metadata schema'),
        ),
        migrations.RunPython(
            move_json_schema_to_foreign_key('CollectionTypeOrganismType', 'metadata_schema')
        ),
        migrations.RemoveField(
            model_name='collectiontypeorganismtype',
            name='metadata_schema',
        ),
        migrations.RenameField(
            model_name='collectiontypeorganismtype',
            old_name='metadata_schema_tmp',
            new_name='metadata_schema',
        ),
        migrations.AddField(
            model_name='organismtype',
            name='identification_info_schema_tmp',
            field=models.ForeignKey(blank=True, db_column='identification_info_schema_id', help_text='JSON Schema for identification information', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='organism_identification_schema', to='irekua_schemas.schema', verbose_name='identification information schema'),
        ),
        migrations.RunPython(
            move_json_schema_to_foreign_key('OrganismType', 'identification_info_schema')
        ),
        migrations.RemoveField(
            model_name='organismtype',
            name='identification_info_schema',
        ),
        migrations.RenameField(
            model_name='organismtype',
            old_name='identification_info_schema_tmp',
            new_name='identification_info_schema',
        ),
    ]
