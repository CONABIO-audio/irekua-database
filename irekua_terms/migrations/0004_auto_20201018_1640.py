# Generated by Django 3.1.2 on 2020-10-18 21:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('irekua_terms', '0003_auto_20201018_1154'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='entailment',
            unique_together={('source', 'target')},
        ),
    ]
