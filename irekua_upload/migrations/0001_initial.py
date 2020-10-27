# Generated by Django 3.1.2 on 2020-10-27 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, db_column='created_on', help_text='Date of creation', verbose_name='created on')),
                ('modified_on', models.DateTimeField(auto_now=True, db_column='modified_on', help_text='Date of last modification', verbose_name='modified on')),
                ('name', models.CharField(db_column='name', help_text='Name of operation', max_length=64, unique=True, verbose_name='name')),
                ('description', models.TextField(db_column='description', help_text='Description of operation', verbose_name='description')),
                ('python_file', models.FileField(blank=True, db_column='python_file', help_text='Python file containing the operation', null=True, upload_to='operations/', verbose_name='python file')),
            ],
            options={
                'verbose_name': 'Operation',
                'verbose_name_plural': 'Operations',
                'ordering': ['-created_on'],
            },
        ),
    ]
