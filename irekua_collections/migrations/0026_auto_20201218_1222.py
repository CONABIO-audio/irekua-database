# Generated by Django 3.1.2 on 2020-12-18 18:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "irekua_collections",
            "0025_change_collection_institution_to_institutions",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="collectionsite",
            name="parent_site",
            field=models.ForeignKey(
                blank=True,
                help_text="Site to which this site belongs if any",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="irekua_collections.collectionsite",
                verbose_name="parent site",
            ),
        ),
    ]
