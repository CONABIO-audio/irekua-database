# Generated by Django 3.1.2 on 2020-10-19 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('irekua_types', '0004_auto_20201018_2307'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='annotationtype',
            options={'ordering': ['-created_on'], 'verbose_name': 'Annotation Type', 'verbose_name_plural': 'Annotation Types'},
        ),
        migrations.AlterModelOptions(
            name='deploymenttype',
            options={'ordering': ['-created_on'], 'verbose_name': 'Deployment Type', 'verbose_name_plural': 'Deployment Types'},
        ),
    ]
