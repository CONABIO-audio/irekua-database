from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('irekua_annotators', '0001_initial'),
        ('irekua_types', '0001_initial'),
        ('irekua_visualizers', '0002_add_visualizer'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='AnnotationTool',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('created_on', models.DateTimeField(auto_now_add=True, db_column='created_on', help_text='Date of creation', verbose_name='created on')),
                        ('modified_on', models.DateTimeField(auto_now=True, db_column='modified_on', help_text='Date of last modification', verbose_name='modified on')),
                        ('name', models.CharField(db_column='name', help_text='Name of annotation tool', max_length=64, verbose_name='name')),
                        ('version', models.CharField(db_column='version', help_text='Version of annotation tool', max_length=16, verbose_name='version')),
                        ('logo', models.ImageField(blank=True, db_column='logo', help_text='Annotation tool logo', null=True, upload_to='images/annotation_tools/', verbose_name='logo')),
                        ('website', models.URLField(blank=True, db_column='website', help_text='Annotation tool website', null=True, verbose_name='website')),
                        ('annotation_type', models.ForeignKey(db_column='annotation_type_id', help_text='Type of annotation this tool produces', on_delete=django.db.models.deletion.CASCADE, to='irekua_types.annotationtype', verbose_name='annotation type')),
                    ],
                    options={
                        'verbose_name': 'Annotation Tool',
                        'verbose_name_plural': 'Annotation Tools',
                        'ordering': ['name'],
                        'unique_together': {('name', 'version')},
                    },
                ),
                migrations.AlterField(
                    model_name='annotationtoolcomponent',
                    name='annotation_tool',
                    field=models.OneToOneField(db_column='annotation_tool_id', help_text='Annotation tool', on_delete=django.db.models.deletion.CASCADE, to='irekua_annotators.AnnotationTool', verbose_name='annotation tool'),
                ),
            ],
            database_operations=[],
        ),
    ]
