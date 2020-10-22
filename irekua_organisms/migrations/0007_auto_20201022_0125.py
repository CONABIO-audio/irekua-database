# Generated by Django 3.1.2 on 2020-10-22 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('irekua_organisms', '0006_add_organism_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organism',
            name='identification_info',
            field=models.JSONField(blank=True, db_column='identification_info', help_text='Organism identification information.', null=True, verbose_name='identification info'),
        ),
    ]
