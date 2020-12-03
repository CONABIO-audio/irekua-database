# Generated by Django 3.1.2 on 2020-12-03 03:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("irekua_geo", "0007_sitetype_icon"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitetype",
            name="can_have_subsites",
            field=models.BooleanField(
                blank=True,
                db_column="can_have_subsites",
                default=False,
                help_text="Determines if sites of this type can have subsites",
                verbose_name="can have subsites",
            ),
        ),
        migrations.AddField(
            model_name="sitetype",
            name="restrict_subsite_types",
            field=models.BooleanField(
                blank=True,
                db_column="restrict_subsite_types",
                default=False,
                help_text="Can any site type be declared as a subsite?",
                verbose_name="restrict subsite types",
            ),
        ),
        migrations.AddField(
            model_name="sitetype",
            name="subsite_types",
            field=models.ManyToManyField(
                blank=True,
                help_text="Site types that can be declared as subsites of sites of this type",
                related_name="_sitetype_subsite_types_+",
                to="irekua_geo.SiteType",
                verbose_name="subsite types",
            ),
        ),
        migrations.AlterField(
            model_name="sitetype",
            name="site_descriptor_types",
            field=models.ManyToManyField(
                blank=True,
                help_text="Descriptor types to be used when describing sites of this type",
                to="irekua_geo.SiteDescriptorType",
                verbose_name="site descriptor types",
            ),
        ),
    ]
