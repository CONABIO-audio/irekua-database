# Generated by Django 3.1.2 on 2020-10-24 23:32

from django.db import migrations, models


def move_event_item_type_relation(apps, schema_editor):
    EventType = apps.get_model("irekua_items", "EventType")
    ItemType = apps.get_model("irekua_items", "ItemType")

    for obj in ItemType.event_types.through.objects.all():
        obj.eventtype.item_types.add(obj.itemtype)

    assert (
        ItemType.event_types.through.objects.count()
        == EventType.item_types.through.objects.count()
    )


class Migration(migrations.Migration):

    dependencies = [
        ("irekua_items", "0007_auto_20201024_1828"),
    ]

    operations = [
        migrations.AddField(
            model_name="eventtype",
            name="item_types",
            field=models.ManyToManyField(
                blank=True,
                db_column="item_types",
                help_text="Types of items in which this event can occur",
                to="irekua_items.ItemType",
                verbose_name="item types",
            ),
        ),
        migrations.RunPython(
            move_event_item_type_relation,
        ),
        migrations.RemoveField(
            model_name="itemtype",
            name="event_types",
        ),
        migrations.RemoveField(
            model_name="item",
            name="ready_event_types",
        ),
    ]
