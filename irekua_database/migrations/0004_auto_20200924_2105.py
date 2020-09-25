# Generated by Django 3.1 on 2020-09-25 02:05

from django.db import migrations, models
import django.db.models.deletion
import irekua_database.utils


def create_user_annotations(apps, schema_editor):
    Annotation = apps.get_model("irekua_database", "Annotation")
    UserAnnotation = apps.get_model("irekua_database", "UserAnnotation")

    current_annotations = Annotation.objects.all().count()

    for annotation in Annotation.objects.all():
        userannotation = UserAnnotation(
            annotation_ptr=annotation,
            visualizer_configuration_tmp=annotation.visualizer_configuration,
            quality_tmp=annotation.quality,
            certainty_tmp=annotation.certainty,
            commentaries_tmp=annotation.commentaries,
            annotation_tool_tmp=annotation.annotation_tool,
            visualizer_tmp=annotation.visualizer)
        userannotation.__dict__.update(annotation.__dict__)
        userannotation.save()

    # No new annotations were created by this migrations
    assert current_annotations == Annotation.objects.all().count()


def recovered_dropped_fields(apps, schema_editor):
    Annotation = apps.get_model("irekua_database", "Annotation")
    UserAnnotation = apps.get_model("irekua_database", "UserAnnotation")

    fields = [
        'visualizer_configuration',
        'quality',
        'certainty',
        'commentaries',
        'annotation_tool',
        'visualizer',
    ]
    objects = []
    for user_annotation in UserAnnotation.objects.all():
        annotation = user_annotation.annotation
        annotation.visualizer_configuration = user_annotation.visualizer_configuration_tmp
        annotation.quality = user_annotation.quality_tmp
        annotation.certainty = user_annotation.certainty_tmp
        annotation.commentaries = user_annotation.commentaries_tmp
        annotation.annotation_tool = user_annotation.annotation_tool_tmp
        annotation.visualizer = user_annotation.visualizer_tmp
        objects.append(annotation)

    Annotation.objects.bulk_update(objects, fields, batch_size=1000)


class Migration(migrations.Migration):

    dependencies = [
        ('irekua_database', '0003_auto_20200826_1946'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAnnotation',
            fields=[
                ('annotation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='irekua_database.annotation')),
                ('visualizer_configuration_tmp', models.JSONField(blank=True, db_column='visualizer_configuration', default=irekua_database.utils.empty_JSON, help_text='Configuration of visualizer at annotation creation', verbose_name='visualizer configuration')),
                ('quality_tmp', models.CharField(blank=True, choices=[('L', 'low'), ('M', 'medium'), ('H', 'high')], db_column='quality', help_text='Quality of item content inside annotation', max_length=16, verbose_name='quality')),
                ('certainty_tmp', models.CharField(blank=True, choices=[('L', 'uncertain'), ('M', 'somewhat certain'), ('H', 'certain')], db_column='certainty', help_text='Level of certainty of location or labelling of annotation', max_length=16, null=True, verbose_name='certainty')),
                ('commentaries_tmp', models.TextField(blank=True, db_column='commentaries', help_text='Commentaries of annotator', verbose_name='commentaries')),
                ('annotation_tool_tmp', models.ForeignKey(db_column='annotation_tool_id', help_text='Annotation tool used when annotating', on_delete=django.db.models.deletion.PROTECT, to='irekua_database.annotationtool', verbose_name='annotation tool')),
                ('visualizer_tmp', models.ForeignKey(db_column='visualizers_id', help_text='Visualizer used when annotating', on_delete=django.db.models.deletion.PROTECT, to='irekua_database.visualizer', verbose_name='visualizer')),
            ],
            options={
                'verbose_name': 'User Annotation',
                'verbose_name_plural': 'User Annotations',
            },
            bases=('irekua_database.annotation',),
        ),
        migrations.RunPython(
            create_user_annotations,
            recovered_dropped_fields,
            atomic=True,
        ),
        migrations.RemoveField(
            model_name='annotation',
            name='annotation_tool',
        ),
        migrations.RemoveField(
            model_name='annotation',
            name='certainty',
        ),
        migrations.RemoveField(
            model_name='annotation',
            name='commentaries',
        ),
        migrations.RemoveField(
            model_name='annotation',
            name='quality',
        ),
        migrations.RemoveField(
            model_name='annotation',
            name='visualizer',
        ),
        migrations.RemoveField(
            model_name='annotation',
            name='visualizer_configuration',
        ),
        migrations.RenameField(
            model_name='userannotation',
            old_name='annotation_tool_tmp',
            new_name='annotation_tool',
        ),
        migrations.RenameField(
            model_name='userannotation',
            old_name='certainty_tmp',
            new_name='certainty',
        ),
        migrations.RenameField(
            model_name='userannotation',
            old_name='commentaries_tmp',
            new_name='commentaries',
        ),
        migrations.RenameField(
            model_name='userannotation',
            old_name='quality_tmp',
            new_name='quality',
        ),
        migrations.RenameField(
            model_name='userannotation',
            old_name='visualizer_tmp',
            new_name='visualizer',
        ),
        migrations.RenameField(
            model_name='userannotation',
            old_name='visualizer_configuration_tmp',
            new_name='visualizer_configuration',
        ),
    ]