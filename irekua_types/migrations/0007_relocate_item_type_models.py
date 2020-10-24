# Generated by Django 3.1.2 on 2020-10-21 23:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('irekua_collections', '0010_update_item_type_reference_to_irekua_items'),
        ('irekua_items', '0004_include_item_types_models'),
        ('irekua_types', '0006_relocate_deployment_and_sampling_event_types'),
        ('irekua_models', '0004_update_types_references'),
        ('selia_annotator', '0003_change_annotation_type_reference'),
        ('selia_visualizers', '0003_change_item_type_reference'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(
                    model_name='eventtype',
                    name='annotation_types',
                ),
                migrations.RemoveField(
                    model_name='eventtype',
                    name='metadata_schema',
                ),
                migrations.RemoveField(
                    model_name='eventtype',
                    name='should_imply',
                ),
                migrations.RemoveField(
                    model_name='eventtype',
                    name='term_types',
                ),
                migrations.RemoveField(
                    model_name='itemtype',
                    name='event_types',
                ),
                migrations.RemoveField(
                    model_name='itemtype',
                    name='metadata_schema',
                ),
                migrations.RemoveField(
                    model_name='itemtype',
                    name='mime_types',
                ),
                migrations.RemoveField(
                    model_name='licencetype',
                    name='metadata_schema',
                ),
                migrations.DeleteModel(
                    name='AnnotationType',
                ),
                migrations.DeleteModel(
                    name='EventType',
                ),
                migrations.DeleteModel(
                    name='ItemType',
                ),
                migrations.DeleteModel(
                    name='LicenceType',
                ),
            ],
            database_operations=[
                migrations.AlterModelTable(
                    name='AnnotationType',
                    table='irekua_items_annotationtype',
                ),
                migrations.AlterModelTable(
                    name='EventType',
                    table='irekua_items_eventtype',
                ),
                migrations.AlterModelTable(
                    name='ItemType',
                    table='irekua_items_itemtype',
                ),
                migrations.AlterModelTable(
                    name='LicenceType',
                    table='irekua_items_licencetype',
                ),
            ],
        ),
    ]
