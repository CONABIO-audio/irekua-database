from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('irekua_models', '0003_update_item_references'),
        ('irekua_items', '0004_include_item_types_models'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='model',
                    name='annotation_type',
                    field=models.ForeignKey(db_column='annotation_type_id', help_text='Type of annotation produced by the model.', on_delete=django.db.models.deletion.CASCADE, to='irekua_items.AnnotationType', verbose_name='annotation type'),
                ),
                migrations.AlterField(
                    model_name='model',
                    name='event_types',
                    field=models.ManyToManyField(blank=True, help_text='Event types that can be detected by the model.', to='irekua_items.EventType'),
                ),
                migrations.AlterField(
                    model_name='model',
                    name='item_types',
                    field=models.ManyToManyField(blank=True, help_text='Item Types that can be processed by the model', to='irekua_items.ItemType'),
                ),
                migrations.AlterField(
                    model_name='modelprediction',
                    name='event_type',
                    field=models.ForeignKey(db_column='event_type_id', help_text='Event predicted by the model.', on_delete=django.db.models.deletion.PROTECT, to='irekua_items.EventType', verbose_name='event type'),
                ),
            ],
            database_operations=[],
        ),
    ]
