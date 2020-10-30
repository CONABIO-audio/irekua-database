# Generated by Django 3.1.2 on 2020-10-25 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('irekua_annotators', '0008_add_annotator_configuration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annotator',
            name='name',
            field=models.CharField(db_column='name', help_text='Name of annotator', max_length=64, unique=True, verbose_name='name'),
        ),
    ]