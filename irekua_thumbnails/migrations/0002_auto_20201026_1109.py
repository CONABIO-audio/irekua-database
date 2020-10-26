# Generated by Django 3.1.2 on 2020-10-26 17:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('irekua_items', '0011_delete_itemthumbnail'),
        ('irekua_thumbnails', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThumbnailCreator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, db_column='created_on', help_text='Date of creation', verbose_name='created on')),
                ('modified_on', models.DateTimeField(auto_now=True, db_column='modified_on', help_text='Date of last modification', verbose_name='modified on')),
                ('name', models.CharField(db_column='name', help_text='Name of thumbnail creator', max_length=64, unique=True, verbose_name='name')),
                ('python_file', models.FileField(db_column='python_file', help_text='Python file containing the thumbnail creator function', upload_to='thumbnail_creators/', verbose_name='python file')),
            ],
            options={
                'verbose_name': 'Thumbnail creator',
                'verbose_name_plural': 'Thumbnail creators',
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='ThumbnailCreatorItemType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, db_column='created_on', help_text='Date of creation', verbose_name='created on')),
                ('modified_on', models.DateTimeField(auto_now=True, db_column='modified_on', help_text='Date of last modification', verbose_name='modified on')),
                ('is_active', models.BooleanField(db_column='is_active', default=True, help_text='Indicates wheter this thumbnail creator should be used as the default thumbnail creator for this item type.', verbose_name='is active')),
                ('item_type', models.ForeignKey(db_column='item_type_id', help_text='Item type that can be processed by this thumbnail creator', on_delete=django.db.models.deletion.CASCADE, to='irekua_items.itemtype', verbose_name='item type')),
                ('thumbnail_creator', models.ForeignKey(db_column='thumbnail_creator_id', help_text='The thumbnail creator that can process items of this type', on_delete=django.db.models.deletion.CASCADE, to='irekua_thumbnails.thumbnailcreator', verbose_name='thumbnail creator')),
            ],
            options={
                'verbose_name': 'Thumbnail Creator Item Type',
                'verbose_name_plural': 'Thumbnail Creator Item Types',
                'ordering': ['-created_on'],
                'unique_together': {('thumbnail_creator', 'item_type')},
            },
        ),
        migrations.AddField(
            model_name='thumbnailcreator',
            name='item_types',
            field=models.ManyToManyField(help_text='Item types that can be processed by this thumbnail creator', through='irekua_thumbnails.ThumbnailCreatorItemType', to='irekua_items.ItemType', verbose_name='item types'),
        ),
    ]
