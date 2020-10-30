# Generated by Django 3.1.2 on 2020-10-25 00:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('irekua_annotations', '0001_initial'),
        ('irekua_collections', '0013_update_annotation_type_reference'),
        ('irekua_annotators', '0004_update_annotation_type_reference'),
        ('irekua_models', '0006_update_annotation_type_reference'),
        ('irekua_items', '0009_add_mime_type'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(
                    model_name='annotationtype',
                    name='annotation_schema',
                ),
                migrations.RemoveField(
                    model_name='annotationtype',
                    name='metadata_schema',
                ),
                migrations.AlterUniqueTogether(
                    name='annotationvote',
                    unique_together=None,
                ),
                migrations.RemoveField(
                    model_name='annotationvote',
                    name='annotation',
                ),
                migrations.RemoveField(
                    model_name='annotationvote',
                    name='created_by',
                ),
                migrations.RemoveField(
                    model_name='annotationvote',
                    name='labels',
                ),
                migrations.RemoveField(
                    model_name='annotationvote',
                    name='modified_by',
                ),
                migrations.RemoveField(
                    model_name='eventtype',
                    name='annotation_types',
                ),
                migrations.RemoveField(
                    model_name='eventtype',
                    name='item_types',
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
                migrations.DeleteModel(
                    name='Annotation',
                ),
                migrations.DeleteModel(
                    name='AnnotationType',
                ),
                migrations.DeleteModel(
                    name='AnnotationVote',
                ),
                migrations.DeleteModel(
                    name='EventType',
                ),
            ],
            database_operations=[
                migrations.AlterModelTable(
                    name='Annotation',
                    table='irekua_annotations_annotation',
                ),
                migrations.AlterModelTable(
                    name='AnnotationType',
                    table='irekua_annotations_annotationtype',
                ),
                migrations.AlterModelTable(
                    name='AnnotationVote',
                    table='irekua_annotations_annotationvote',
                ),
                migrations.AlterModelTable(
                    name='EventType',
                    table='irekua_annotations_eventtype',
                ),
            ]
        ),
    ]
