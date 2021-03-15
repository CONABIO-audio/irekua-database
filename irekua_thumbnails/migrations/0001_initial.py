# Generated by Django 3.1.2 on 2020-10-26 15:28

from django.db import migrations, models
import django.db.models.deletion
import irekua_thumbnails.models.thumbnails
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("irekua_items", "0010_relocate_annotation_models"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name="ItemThumbnail",
                    fields=[
                        (
                            "created_on",
                            models.DateTimeField(
                                auto_now_add=True,
                                db_column="created_on",
                                help_text="Date of creation",
                                verbose_name="created on",
                            ),
                        ),
                        (
                            "modified_on",
                            models.DateTimeField(
                                auto_now=True,
                                db_column="modified_on",
                                help_text="Date of last modification",
                                verbose_name="modified on",
                            ),
                        ),
                        (
                            "item",
                            models.OneToOneField(
                                db_column="item_id",
                                help_text="Item whose thumbnail is this.",
                                on_delete=django.db.models.deletion.CASCADE,
                                primary_key=True,
                                serialize=False,
                                to="irekua_items.item",
                                verbose_name="item",
                            ),
                        ),
                        (
                            "thumbnail",
                            sorl.thumbnail.fields.ImageField(
                                db_column="thumbnail",
                                help_text="Thumbnail associated to item",
                                upload_to=irekua_thumbnails.models.thumbnails.get_thumbnail_path,
                                verbose_name="thumbnail",
                            ),
                        ),
                    ],
                    options={
                        "verbose_name": "Item Thumbnail",
                        "verbose_name_plural": "Items Thumbnails",
                        "ordering": ["created_on"],
                    },
                ),
            ],
            database_operations=[],
        ),
    ]
