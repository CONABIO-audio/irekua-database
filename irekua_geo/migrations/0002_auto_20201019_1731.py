# Generated by Django 3.1.2 on 2020-10-19 22:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('irekua_geo', '0001_initial'),
        ('irekua_database', '0014_massive_migration_to_submodules'),
    ]

    operations = [
        migrations.AddField(
            model_name='locality',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, db_column='created_on', default=django.utils.timezone.now, help_text='Date of creation', verbose_name='created on'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='locality',
            name='modified_on',
            field=models.DateTimeField(auto_now=True, db_column='modified_on', help_text='Date of last modification', verbose_name='modified on'),
        ),
    ]
