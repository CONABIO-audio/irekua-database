# Generated by Django 2.2.7 on 2019-11-25 15:34
import os
from django.db import migrations, models
import django.db.models.deletion


def annotator_path(instance, filename):
    _, ext = os.path.splitext(filename)
    return 'annotators/{name}_{version}.{ext}'.format(
        name=instance.annotation_tool.name.replace(' ', '_'),
        version=instance.annotation_tool.version.replace('.', '_'),
        ext=ext)


def check_name_change(apps, schema_editor):
    sql = "SELECT * FROM django_content_type WHERE app_label='selia_annotator'"

    with schema_editor.connection.cursor() as cursor:
        cursor.execute(sql, ())

        if cursor.fetchone():
            msg = 'Please run the script `change_app_names` before continuing migrations'
            raise ValueError(msg)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('irekua_database', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnnotationToolComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('javascript_file', models.FileField(db_column='javascript_file', help_text='Javascript file containing annotator component', upload_to=annotator_path, verbose_name='javascript file')),
                ('is_active', models.BooleanField(db_column='is_active', default=True, help_text='Is annotator tool active?', verbose_name='is active')),
                ('annotation_tool', models.OneToOneField(db_column='annotation_tool_id', help_text='Annotation tool', on_delete=django.db.models.deletion.CASCADE, to='irekua_database.AnnotationTool', verbose_name='annotation tool')),
            ],
            options={
                'verbose_name': 'Annotation Tool Component',
                'verbose_name_plural': 'Annotation Tool Components',
            },
        ),
        migrations.RunPython(
            check_name_change
        )
    ]