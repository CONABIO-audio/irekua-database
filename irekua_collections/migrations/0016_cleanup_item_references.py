# Generated by Django 3.1.2 on 2020-10-27 22:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('irekua_collections', '0015_add_site_and_device_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='samplingeventitem',
            name='collectionitem_ptr',
        ),
        migrations.AlterField(
            model_name='deploymentitem',
            name='deviceitem_ptr',
            field=models.OneToOneField(auto_created=True, default=None, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=False, serialize=False, to='irekua_collections.deviceitem'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='deploymentitem',
            name='samplingeventitem_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=False, to='irekua_collections.samplingeventitem'),
        ),
        migrations.AlterField(
            model_name='samplingeventitem',
            name='siteitem_ptr',
            field=models.OneToOneField(auto_created=True, default=None, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=False, serialize=False, to='irekua_collections.siteitem'),
            preserve_default=False,
        ),
    ]