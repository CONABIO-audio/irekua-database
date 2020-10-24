from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('selia_visualizers', '0001_initial'),
        ('irekua_types', '0001_initial'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='Visualizer',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('created_on', models.DateTimeField(auto_now_add=True, db_column='created_on', help_text='Date of creation', verbose_name='created on')),
                        ('modified_on', models.DateTimeField(auto_now=True, db_column='modified_on', help_text='Date of last modification', verbose_name='modified on')),
                        ('name', models.CharField(db_column='name', help_text='Name of visualizer app', max_length=64, verbose_name='name')),
                        ('version', models.CharField(db_column='version', help_text='Version of visualizer app', max_length=16, verbose_name='version')),
                        ('website', models.URLField(blank=True, db_column='website', help_text='Link to visualizer website', verbose_name='website')),
                        ('configuration_schema', models.JSONField(blank=True, db_column='configuration_schema', help_text='JSON schema for annotation tool configuration info', verbose_name='configuration schema')),
                    ],
                    options={
                        'verbose_name': 'Visualizer',
                        'verbose_name_plural': 'Visualizers',
                        'ordering': ['-created_on'],
                        'unique_together': {('name', 'version')},
                    },
                ),
                migrations.AlterField(
                    model_name='visualizercomponent',
                    name='visualizer',
                    field=models.OneToOneField(db_column='visualizer_id', help_text='Visualizer', on_delete=django.db.models.deletion.CASCADE, to='selia_visualizers.visualizer', verbose_name='visualizer'),
                ),
                migrations.AlterField(
                    model_name='visualizercomponentitemtype',
                    name='item_type',
                    field=models.ForeignKey(db_column='item_type_id', help_text='Item type', on_delete=django.db.models.deletion.CASCADE, to='irekua_types.ItemType', verbose_name='item type'),
                ),
                migrations.AlterField(
                    model_name='visualizercomponent',
                    name='item_types',
                    field=models.ManyToManyField(through='selia_visualizers.VisualizerComponentItemType', to='irekua_types.ItemType'),
                ),
            ],
            database_operations=[],
        ),
    ]
