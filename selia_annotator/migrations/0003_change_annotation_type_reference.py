from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('selia_annotator', '0002_add_annotator'),
        ('irekua_items', '0004_include_item_types_models'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='annotationtool',
                    name='annotation_type',
                    field=models.ForeignKey(db_column='annotation_type_id', help_text='Type of annotation this tool produces', on_delete=django.db.models.deletion.CASCADE, to='irekua_items.annotationtype', verbose_name='annotation type'),
                ),
            ],
            database_operations=[],
        ),
    ]
