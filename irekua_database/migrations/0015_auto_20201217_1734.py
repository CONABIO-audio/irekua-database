# Generated by Django 3.1.2 on 2020-12-17 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('irekua_database', '0014_auto_20201017_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='permissions',
            field=models.ManyToManyField(blank=True, help_text='Permissions associated to role', to='auth.Permission', verbose_name='permissions'),
        ),
    ]
