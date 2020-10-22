from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('irekua_models', '0002_update_term_references'),
        ('irekua_types', '0001_initial'),
        ('irekua_items', '0001_initial'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='model',
                    name='annotation_type',
                    field=models.ForeignKey(db_column='annotation_type_id', help_text='Type of annotation produced by the model.', on_delete=django.db.models.deletion.CASCADE, to='irekua_types.AnnotationType', verbose_name='annotation type'),
                ),
                migrations.AlterField(
                    model_name='model',
                    name='event_types',
                    field=models.ManyToManyField(blank=True, help_text='Event types that can be detected by the model.', to='irekua_types.EventType'),
                ),
                migrations.AlterField(
                    model_name='model',
                    name='item_types',
                    field=models.ManyToManyField(blank=True, help_text='Item Types that can be processed by the model', to='irekua_types.ItemType'),
                ),
                migrations.AlterField(
                    model_name='modelprediction',
                    name='event_type',
                    field=models.ForeignKey(db_column='event_type_id', help_text='Event predicted by the model.', on_delete=django.db.models.deletion.PROTECT, to='irekua_types.EventType', verbose_name='event type'),
                ),
                migrations.AlterField(
                    model_name='modelprediction',
                    name='item',
                    field=models.ForeignKey(db_column='item_id', help_text='Item on which the prediction was made.', on_delete=django.db.models.deletion.CASCADE, to='irekua_items.Item', verbose_name='item'),
                ),
            ],
            database_operations=[],
        ),
    ]
