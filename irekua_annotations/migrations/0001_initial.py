# Generated by Django 3.1.2 on 2020-10-25 00:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import irekua_database.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('irekua_visualizers', '0004_auto_20201024_1826'),
        ('irekua_schemas', '0002_auto_20201018_2158'),
        ('irekua_items', '0009_add_mime_type'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('irekua_annotators', '0003_change_annotation_type_reference'),
        ('irekua_terms', '0006_auto_20201021_2015'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='AnnotationType',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('created_on', models.DateTimeField(auto_now_add=True, db_column='created_on', help_text='Date of creation', verbose_name='created on')),
                        ('modified_on', models.DateTimeField(auto_now=True, db_column='modified_on', help_text='Date of last modification', verbose_name='modified on')),
                        ('name', models.CharField(db_column='name', help_text='Name for type of annotation', max_length=64, unique=True, verbose_name='name')),
                        ('description', models.TextField(db_column='description', help_text='Description of annotation type', verbose_name='description')),
                        ('icon', models.ImageField(blank=True, db_column='icon', help_text='Annotation type icon', null=True, upload_to='images/annotation_types/', verbose_name='icon')),
                        ('annotation_schema', models.ForeignKey(blank=True, db_column='annotation_schema_id', help_text='JSON Schema for annotation info', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='annotation_schema', to='irekua_schemas.schema', verbose_name='annotation schema')),
                        ('metadata_schema', models.ForeignKey(blank=True, db_column='metadata_schema_id', help_text='JSON Schema for additional metadata', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='annotationtype_metadata_schema', to='irekua_schemas.schema', verbose_name='metadata schema')),
                    ],
                    options={
                        'verbose_name': 'Annotation Type',
                        'verbose_name_plural': 'Annotation Types',
                        'ordering': ['-created_on'],
                    },
                ),
                migrations.CreateModel(
                    name='EventType',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('created_on', models.DateTimeField(auto_now_add=True, db_column='created_on', help_text='Date of creation', verbose_name='created on')),
                        ('modified_on', models.DateTimeField(auto_now=True, db_column='modified_on', help_text='Date of last modification', verbose_name='modified on')),
                        ('name', models.CharField(db_column='name', help_text='Name of event type', max_length=64, unique=True, verbose_name='name')),
                        ('description', models.TextField(db_column='description', help_text='Description of event type', verbose_name='description')),
                        ('icon', models.ImageField(blank=True, db_column='icon', help_text='Event type icon', null=True, upload_to='images/event_types/', verbose_name='icon')),
                        ('restrict_annotation_types', models.BooleanField(db_column='restrict_annotation_types', default=False, help_text='Flag indicating whether to restrict annotation types apt for this event type', verbose_name='restrict annotation types')),
                        ('annotation_types', models.ManyToManyField(blank=True, help_text='Valid annotation types for this event type', to='irekua_annotations.AnnotationType', verbose_name='annotation types')),
                        ('item_types', models.ManyToManyField(blank=True, db_column='item_types', help_text='Types of items in which this event can occur', to='irekua_items.ItemType', verbose_name='item types')),
                        ('metadata_schema', models.ForeignKey(blank=True, db_column='metadata_schema_id', help_text='JSON Schema for additional metadata', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='eventtype_metadata_schema', to='irekua_schemas.schema', verbose_name='metadata schema')),
                        ('should_imply', models.ManyToManyField(blank=True, db_column='should_imply', help_text='Terms that should be implied (if meaningful) by any terms used to describe this event type.', to='irekua_terms.Term', verbose_name='should imply')),
                        ('term_types', models.ManyToManyField(blank=True, db_column='term_types', help_text='Valid term types with which to label this type of events', to='irekua_terms.TermType', verbose_name='term types')),
                    ],
                    options={
                        'verbose_name': 'Event Type',
                        'verbose_name_plural': 'Event Types',
                        'ordering': ['name'],
                    },
                ),
                migrations.CreateModel(
                    name='Annotation',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('created_on', models.DateTimeField(auto_now_add=True, db_column='created_on', help_text='Date of creation', verbose_name='created on')),
                        ('modified_on', models.DateTimeField(auto_now=True, db_column='modified_on', help_text='Date of last modification', verbose_name='modified on')),
                        ('annotation', models.JSONField(blank=True, db_column='annotation', default=irekua_database.utils.empty_JSON, help_text='Information of annotation location within item', verbose_name='annotation')),
                        ('visualizer_configuration', models.JSONField(blank=True, db_column='visualizer_configuration', default=irekua_database.utils.empty_JSON, help_text='Configuration of visualizer at annotation creation', verbose_name='visualizer configuration')),
                        ('certainty', models.CharField(blank=True, choices=[('L', 'uncertain'), ('M', 'somewhat certain'), ('H', 'certain')], db_column='certainty', help_text='Level of certainty of location or labelling of annotation', max_length=16, null=True, verbose_name='certainty')),
                        ('quality', models.CharField(blank=True, choices=[('L', 'low'), ('M', 'medium'), ('H', 'high')], db_column='quality', help_text='Quality of item content inside annotation', max_length=16, verbose_name='quality')),
                        ('commentaries', models.TextField(blank=True, db_column='commentaries', help_text='Commentaries of annotator', verbose_name='commentaries')),
                        ('annotation_tool', models.ForeignKey(db_column='annotation_tool_id', help_text='Annotation tool used when annotating', on_delete=django.db.models.deletion.PROTECT, to='irekua_annotators.annotationtool', verbose_name='annotation tool')),
                        ('annotation_type', models.ForeignKey(db_column='annotation_type_id', help_text='Type of annotation', on_delete=django.db.models.deletion.PROTECT, to='irekua_annotations.annotationtype', verbose_name='annotation type')),
                        ('created_by', models.ForeignKey(blank=True, db_column='creator_id', help_text='Creator of object', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='annotation_created_by', to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                        ('event_type', models.ForeignKey(db_column='event_type_id', help_text='Type of event being annotated', on_delete=django.db.models.deletion.PROTECT, to='irekua_annotations.eventtype', verbose_name='event type')),
                        ('item', models.ForeignKey(db_column='item_id', help_text='Annotated item', on_delete=django.db.models.deletion.PROTECT, to='irekua_items.item', verbose_name='item')),
                        ('labels', models.ManyToManyField(blank=True, db_column='labels', help_text='Labels associated with annotation', to='irekua_terms.Term', verbose_name='labels')),
                        ('modified_by', models.ForeignKey(blank=True, db_column='modified_by', editable=False, help_text='User who made modifications last', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='annotation_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='modified by')),
                        ('visualizer', models.ForeignKey(db_column='visualizers_id', help_text='Visualizer used when annotating', on_delete=django.db.models.deletion.PROTECT, to='irekua_visualizers.visualizer', verbose_name='visualizer')),
                    ],
                    options={
                        'verbose_name': 'Annotation',
                        'verbose_name_plural': 'Annotations',
                        'ordering': ['-modified_on'],
                        'permissions': (('vote', 'Can vote annotation'),),
                    },
                ),
                migrations.CreateModel(
                    name='AnnotationVote',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('created_on', models.DateTimeField(auto_now_add=True, db_column='created_on', help_text='Date of creation', verbose_name='created on')),
                        ('modified_on', models.DateTimeField(auto_now=True, db_column='modified_on', help_text='Date of last modification', verbose_name='modified on')),
                        ('incorrect_geometry', models.BooleanField(blank=True, db_column='incorrect_geometry', default=False, help_text='Is the annotation geometry incorrect?', verbose_name='incorrect geometry')),
                        ('annotation', models.ForeignKey(db_column='annotation_id', help_text='Reference to annotation being voted', on_delete=django.db.models.deletion.CASCADE, to='irekua_annotations.annotation', verbose_name='annotation')),
                        ('created_by', models.ForeignKey(blank=True, db_column='creator_id', help_text='Creator of object', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='annotationvote_created_by', to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                        ('labels', models.ManyToManyField(blank=True, db_column='labels', help_text='Labels associated with annotation', to='irekua_terms.Term', verbose_name='labels')),
                        ('modified_by', models.ForeignKey(blank=True, db_column='modified_by', editable=False, help_text='User who made modifications last', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='annotationvote_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='modified by')),
                    ],
                    options={
                        'verbose_name': 'Annotation Vote',
                        'verbose_name_plural': 'Annotation Votes',
                        'ordering': ['-created_on'],
                        'unique_together': {('annotation', 'created_by')},
                    },
                ),
            ],
            database_operations=[],
        ),
    ]
