# Generated by Django 3.1 on 2021-03-05 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("irekua_devices", "0009_update_mime_type_field_description"),
        ("irekua_items", "0016_auto_20210305_0737"),
        ("irekua_upload", "0002_mediainfoextractor"),
    ]

    operations = [
        migrations.AddField(
            model_name="mediainfoextractor",
            name="device_types",
            field=models.ManyToManyField(
                help_text="If empty this extractor should work on any device type.Otherwise list the device types on which this extractorworks.",
                to="irekua_devices.DeviceType",
            ),
        ),
        migrations.AddField(
            model_name="mediainfoextractor",
            name="devices",
            field=models.ManyToManyField(
                help_text="If empty this extractor should work on any device.Otherwise list the devices on which this extractor works.",
                to="irekua_devices.Device",
            ),
        ),
        migrations.AddField(
            model_name="mediainfoextractor",
            name="item_types",
            field=models.ManyToManyField(
                help_text="If empty this extractor should work on any item type.Otherwise list the item types on which this extractorworks.",
                to="irekua_items.ItemType",
            ),
        ),
        migrations.AddField(
            model_name="mediainfoextractor",
            name="javascript_file",
            field=models.FileField(
                blank=True,
                db_column="javascript_file",
                help_text="Javascript file containing the media info extractor function",
                null=True,
                upload_to="media_info_extractors/",
                verbose_name="javascript file",
            ),
        ),
        migrations.AddField(
            model_name="mediainfoextractor",
            name="mime_type",
            field=models.ForeignKey(
                db_column="mime_type_id",
                default=None,
                help_text="Mime type of files on which this extractor operates.",
                on_delete=django.db.models.deletion.CASCADE,
                to="irekua_items.mimetype",
                verbose_name="mime type",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="mediainfoextractor",
            name="name",
            field=models.CharField(
                db_column="name",
                default=None,
                help_text="Name of the media info extractor",
                max_length=64,
                unique=True,
                verbose_name="name",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="mediainfoextractor",
            name="media_info_type",
            field=models.ForeignKey(
                db_column="media_info_type_id",
                help_text="Media info type that can be extracted by this extractor",
                on_delete=django.db.models.deletion.CASCADE,
                to="irekua_items.mediainfotype",
                verbose_name="media info type",
            ),
        ),
        migrations.AlterField(
            model_name="mediainfoextractor",
            name="python_file",
            field=models.FileField(
                blank=True,
                db_column="python_file",
                help_text="Python file containing the media info extractor function",
                null=True,
                upload_to="media_info_extractors/",
                verbose_name="python file",
            ),
        ),
    ]