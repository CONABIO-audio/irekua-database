# Generated by Django 3.1 on 2020-09-25 21:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('irekua_database', '0006_delete_annotationtool'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(
                    name='Visualizer',
                ),
            ],
            database_operations=[
                migrations.AlterModelTable(
                    name='Visualizer',
                    table='selia_visualizers_visualizer',
                ),
            ]
        )
    ]