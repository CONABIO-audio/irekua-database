from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('selia_visualizers', '0002_add_visualizer'),
        ('irekua_items', '0004_include_item_types_models'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='visualizercomponentitemtype',
                    name='item_type',
                    field=models.ForeignKey(db_column='item_type_id', help_text='Item type', on_delete=django.db.models.deletion.CASCADE, to='irekua_items.ItemType', verbose_name='item type'),
                ),
                migrations.AlterField(
                    model_name='visualizercomponent',
                    name='item_types',
                    field=models.ManyToManyField(through='selia_visualizers.VisualizerComponentItemType', to='irekua_items.ItemType'),
                ),
            ],
            database_operations=[],
        ),
    ]
