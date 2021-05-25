# Generated by Django 3.1.2 on 2020-10-22 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("irekua_devices", "0004_include_device_type_models"),
    ]

    operations = [
        migrations.AlterField(
            model_name="physicaldevice",
            name="metadata",
            field=models.JSONField(
                blank=True,
                db_column="metadata",
                help_text="Metadata associated to device",
                null=True,
                verbose_name="metadata",
            ),
        ),
    ]
