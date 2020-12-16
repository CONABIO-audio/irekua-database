# Generated by Django 3.1.2 on 2020-12-16 01:12

from tqdm import tqdm
from django.db import migrations, models
import django.db.models.deletion


SQL_QUERY = """
SELECT
    depi.deployment_item_id,
    depi.deployment_id,
    sei.sampling_event_id,
    devi.collection_device_id,
    siti.collection_site_id,
    coli.collection_id,
    coli.collection_metadata,
    it.id
FROM irekua_collections_deploymentitem as depi
    LEFT JOIN
    irekua_collections_samplingeventitem as sei
    ON depi.samplingeventitem_ptr_id = sei.sampling_event_item_id
        LEFT JOIN
        irekua_collections_siteitem as siti
        ON sei.siteitem_ptr_id = siti.siteitem_id
    LEFT JOIN
    irekua_collections_deviceitem as devi
    ON depi.deviceitem_ptr_id = devi.deviceitem_id
        LEFT JOIN
        irekua_collections_collectionitem as coli
        ON devi.device_item_id = coli.collection_item_id
            LEFT JOIN
            irekua_items_item as it
            ON coli.item_ptr_id = it.id
"""


def migrate_items(apps, schema_editor):
    Item = apps.get_model(
        "irekua_items",
        "Item",
    )

    CollectionItemTmp = apps.get_model(
        "irekua_collections",
        "CollectionItemTmp",
    )

    CollectionItem = apps.get_model(
        "irekua_collections",
        "CollectionItem",
    )

    DeploymentItem = apps.get_model(
        "irekua_collections",
        "DeploymentItem",
    )

    items_count = CollectionItem.objects.count()
    assert DeploymentItem.objects.count() == items_count

    queryset = DeploymentItem.objects.raw(SQL_QUERY)
    for data in tqdm(queryset, total=items_count):
        item_ptr = Item.objects.get(id=data.id)
        item = CollectionItemTmp(
            item_ptr=item_ptr,
            collection_id=data.collection_id,
            collection_metadata=data.collection_metadata,
            sampling_event_id=data.sampling_event_id,
            deployment_id=data.deployment_id,
            collection_site_id=data.collection_site_id,
            collection_device_id=data.collection_device_id,
        )
        item.__dict__.update(item_ptr.__dict__)
        item.save()

    assert CollectionItemTmp.objects.count() == DeploymentItem.objects.count()


class Migration(migrations.Migration):

    dependencies = [
        ("irekua_items", "0013_mediainfoextractor"),
        ("irekua_collections", "0021_auto_20201203_1407"),
    ]

    operations = [
        migrations.CreateModel(
            name="CollectionItemTmp",
            fields=[
                (
                    "item_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="irekua_items.item",
                    ),
                ),
                (
                    "collection_metadata",
                    models.JSONField(
                        blank=True,
                        db_column="collection_metadata",
                        help_text=(
                            "Additional metadata associated "
                            "to item in collection"
                        ),
                        null=True,
                        verbose_name="collection metadata",
                    ),
                ),
            ],
            options={
                "verbose_name": "Collection Item",
                "verbose_name_plural": "Collection Items",
            },
            bases=("irekua_items.item",),
        ),
        migrations.AddField(
            model_name="collectionitemtmp",
            name="collection",
            field=models.ForeignKey(
                blank=True,
                db_column="collection_id",
                help_text="Collection to which this item belongs",
                on_delete=django.db.models.deletion.PROTECT,
                to="irekua_collections.collection",
                verbose_name="collection",
            ),
        ),
        migrations.AddField(
            model_name="collectionitemtmp",
            name="collection_device",
            field=models.ForeignKey(
                blank=True,
                db_column="collection_device_id",
                help_text="Device used to capture the item",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="irekua_collections.collectiondevice",
                verbose_name="collection device",
            ),
        ),
        migrations.AddField(
            model_name="collectionitemtmp",
            name="collection_site",
            field=models.ForeignKey(
                blank=True,
                db_column="collection_site_id",
                help_text="Site in which this item was captured",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="irekua_collections.collectionsite",
                verbose_name="collection site",
            ),
        ),
        migrations.AddField(
            model_name="collectionitemtmp",
            name="deployment",
            field=models.ForeignKey(
                blank=True,
                db_column="deployment_id",
                help_text=(
                    "Deployment of device in which this item was captured"
                ),
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="irekua_collections.deployment",
                verbose_name="deployment",
            ),
        ),
        migrations.AddField(
            model_name="collectionitemtmp",
            name="sampling_event",
            field=models.ForeignKey(
                blank=True,
                db_column="sampling_event_id",
                help_text="Sampling event in which this item was captured",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="irekua_collections.samplingevent",
                verbose_name="sampling event",
            ),
        ),
        migrations.RunPython(
            migrate_items,
        ),
    ]
