# Generated by Django 3.1 on 2021-03-05 13:37

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('irekua_geo', '0009_change_locality_to_localities'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='site',
            unique_together={('name', 'created_by')},
        ),
    ]
