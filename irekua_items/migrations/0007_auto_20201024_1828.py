# Generated by Django 3.1.2 on 2020-10-24 23:28

from django.db import migrations, models
import irekua_database.utils


class Migration(migrations.Migration):

    dependencies = [
        ("irekua_items", "0006_auto_20201021_2034"),
    ]

    operations = [
        migrations.AlterField(
            model_name="annotation",
            name="annotation",
            field=models.JSONField(
                blank=True,
                db_column="annotation",
                default=irekua_database.utils.empty_JSON,
                help_text="Information of annotation location within item",
                verbose_name="annotation",
            ),
        ),
        migrations.AlterField(
            model_name="annotation",
            name="visualizer_configuration",
            field=models.JSONField(
                blank=True,
                db_column="visualizer_configuration",
                default=irekua_database.utils.empty_JSON,
                help_text="Configuration of visualizer at annotation creation",
                verbose_name="visualizer configuration",
            ),
        ),
    ]