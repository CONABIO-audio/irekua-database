# Generated by Django 3.1.2 on 2020-10-22 01:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("irekua_terms", "0005_auto_20201018_1704"),
    ]

    operations = [
        migrations.AlterField(
            model_name="synonym",
            name="metadata",
            field=models.JSONField(
                blank=True,
                db_column="metadata",
                help_text="Metadata associated to the synonym",
                null=True,
                verbose_name="metadata",
            ),
        ),
        migrations.AlterField(
            model_name="synonymsuggestion",
            name="metadata",
            field=models.JSONField(
                blank=True,
                db_column="metadata",
                help_text="Metadata associated to synonym",
                null=True,
                verbose_name="metadata",
            ),
        ),
        migrations.AlterField(
            model_name="synonymsuggestion",
            name="source",
            field=models.ForeignKey(
                db_column="source_id",
                on_delete=django.db.models.deletion.CASCADE,
                to="irekua_terms.term",
                verbose_name="source",
            ),
        ),
        migrations.AlterField(
            model_name="term",
            name="metadata",
            field=models.JSONField(
                blank=True,
                db_column="metadata",
                help_text="Metadata associated to term",
                null=True,
                verbose_name="metadata",
            ),
        ),
        migrations.AlterField(
            model_name="termsuggestion",
            name="metadata",
            field=models.JSONField(
                blank=True,
                db_column="metadata",
                help_text="Metadata associated to term",
                null=True,
                verbose_name="metadata",
            ),
        ),
    ]
