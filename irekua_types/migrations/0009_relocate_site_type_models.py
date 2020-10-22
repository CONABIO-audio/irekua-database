# Generated by Django 3.1.2 on 2020-10-22 00:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('irekua_geo', '0003_include_site_type_models'),
        ('irekua_collections', '0012_update_site_type_models_reference'),
        ('irekua_types', '0008_relocate_device_type_models'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(
                    model_name='sitedescriptortype',
                    name='metadata_schema',
                ),
                migrations.RemoveField(
                    model_name='sitetype',
                    name='metadata_schema',
                ),
                migrations.RemoveField(
                    model_name='sitetype',
                    name='site_descriptor_types',
                ),
                migrations.DeleteModel(
                    name='LocalityType',
                ),
                migrations.DeleteModel(
                    name='SiteDescriptorType',
                ),
                migrations.DeleteModel(
                    name='SiteType',
                ),
            ],
            database_operations=[
                migrations.AlterModelTable(
                    name='LocalityType',
                    table='irekua_geo_localitytype',
                ),
                migrations.AlterModelTable(
                    name='SiteDescriptorType',
                    table='irekua_geo_sitedescriptortype',
                ),
                migrations.AlterModelTable(
                    name='SiteType',
                    table='irekua_geo_sitetype',
                ),
            ],
        ),
    ]
