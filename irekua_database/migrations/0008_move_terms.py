# Generated by Django 3.1 on 2020-10-12 00:03

from django.db import migrations, models
import irekua_database.utils


class Migration(migrations.Migration):

    dependencies = [
        ('irekua_database', '0007_delete_visualizer'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterUniqueTogether(
                    name='entailmenttype',
                    unique_together=None,
                ),
                migrations.RemoveField(
                    model_name='entailmenttype',
                    name='source_type',
                ),
                migrations.RemoveField(
                    model_name='entailmenttype',
                    name='target_type',
                ),
                migrations.RemoveField(
                    model_name='synonym',
                    name='source',
                ),
                migrations.RemoveField(
                    model_name='synonym',
                    name='target',
                ),
                migrations.RemoveField(
                    model_name='synonymsuggestion',
                    name='created_by',
                ),
                migrations.RemoveField(
                    model_name='synonymsuggestion',
                    name='modified_by',
                ),
                migrations.RemoveField(
                    model_name='synonymsuggestion',
                    name='source',
                ),
                migrations.AlterUniqueTogether(
                    name='term',
                    unique_together=None,
                ),
                migrations.RemoveField(
                    model_name='term',
                    name='term_type',
                ),
                migrations.RemoveField(
                    model_name='termsuggestion',
                    name='created_by',
                ),
                migrations.RemoveField(
                    model_name='termsuggestion',
                    name='modified_by',
                ),
                migrations.RemoveField(
                    model_name='termsuggestion',
                    name='term_type',
                ),
                migrations.AlterField(
                    model_name='annotation',
                    name='annotation',
                    field=models.JSONField(blank=True, db_column='annotation', default=irekua_database.utils.empty_JSON, help_text='Information of annotation location within item', verbose_name='annotation'),
                ),
                migrations.AlterField(
                    model_name='annotation',
                    name='labels',
                    field=models.ManyToManyField(blank=True, db_column='labels', help_text='Labels associated with annotation', to='irekua_terms.Term', verbose_name='labels'),
                ),
                migrations.AlterField(
                    model_name='annotationtype',
                    name='annotation_schema',
                    field=models.JSONField(blank=True, db_column='annotation_schema', default=irekua_database.utils.simple_JSON_schema, help_text='JSON Schema for annotation info', validators=[irekua_database.utils.validate_JSON_schema], verbose_name='annotation schema'),
                ),
                migrations.AlterField(
                    model_name='annotationvote',
                    name='labels',
                    field=models.ManyToManyField(blank=True, db_column='labels', help_text='Labels associated with annotation', to='irekua_terms.Term', verbose_name='labels'),
                ),
                migrations.AlterField(
                    model_name='collection',
                    name='metadata',
                    field=models.JSONField(blank=True, db_column='metadata', default=irekua_database.utils.empty_JSON, help_text='Metadata associated to collection', verbose_name='metadata'),
                ),
                migrations.AlterField(
                    model_name='collectiondevice',
                    name='metadata',
                    field=models.JSONField(blank=True, db_column='metadata', default=irekua_database.utils.empty_JSON, help_text='Metadata associated with device within collection', null=True, verbose_name='metadata'),
                ),
                migrations.AlterField(
                    model_name='collectiondevicetype',
                    name='metadata_schema',
                    field=models.JSONField(blank=True, db_column='metadata_schema', default=irekua_database.utils.simple_JSON_schema, help_text='JSON Schema for metadata of collection device info', validators=[irekua_database.utils.validate_JSON_schema], verbose_name='metadata schema'),
                ),
                migrations.AlterField(
                    model_name='collectionitemtype',
                    name='metadata_schema',
                    field=models.JSONField(blank=True, db_column='metadata_schema', default=irekua_database.utils.simple_JSON_schema, help_text='JSON Schema for metadata of collection item info', validators=[irekua_database.utils.validate_JSON_schema], verbose_name='metadata schema'),
                ),
                migrations.AlterField(
                    model_name='collectionrole',
                    name='metadata_schema',
                    field=models.JSONField(blank=True, db_column='metadata_schema', default=irekua_database.utils.simple_JSON_schema, help_text='JSON Schema for metadata of collection role info', validators=[irekua_database.utils.validate_JSON_schema], verbose_name='metadata schema'),
                ),
                migrations.AlterField(
                    model_name='collectionsite',
                    name='metadata',
                    field=models.JSONField(blank=True, db_column='metadata', default=irekua_database.utils.empty_JSON, help_text='Metadata associated to site in collection', null=True, verbose_name='metadata'),
                ),
                migrations.AlterField(
                    model_name='collectiontype',
                    name='metadata_schema',
                    field=models.JSONField(blank=True, db_column='metadata_schema', default=irekua_database.utils.simple_JSON_schema, help_text='JSON Schema for metadata of collection info', validators=[irekua_database.utils.validate_JSON_schema], verbose_name='metadata schema'),
                ),
                migrations.AlterField(
                    model_name='collectionuser',
                    name='metadata',
                    field=models.JSONField(blank=True, db_column='metadata', default=irekua_database.utils.empty_JSON, help_text='Metadata associated to user in collection', null=True, verbose_name='metadata'),
                ),
                migrations.AlterField(
                    model_name='device',
                    name='configuration_schema',
                    field=models.JSONField(blank=True, db_column='configuration_schema', default=irekua_database.utils.simple_JSON_schema, help_text='JSON Schema for configuration info of device', validators=[irekua_database.utils.validate_JSON_schema], verbose_name='configuration schema'),
                ),
                migrations.AlterField(
                    model_name='device',
                    name='metadata_schema',
                    field=models.JSONField(blank=True, db_column='metadata_schema', default=irekua_database.utils.simple_JSON_schema, help_text='JSON Schema for metadata of device info', validators=[irekua_database.utils.validate_JSON_schema], verbose_name='metadata schema'),
                ),
                migrations.AlterField(
                    model_name='eventtype',
                    name='should_imply',
                    field=models.ManyToManyField(blank=True, db_column='should_imply', help_text='Terms that should be implied (if meaningful) by any terms used to describe this event type.', to='irekua_terms.Term', verbose_name='should imply'),
                ),
                migrations.AlterField(
                    model_name='eventtype',
                    name='term_types',
                    field=models.ManyToManyField(blank=True, db_column='term_types', help_text='Valid term types with which to label this type of events', to='irekua_terms.TermType', verbose_name='term types'),
                ),
                migrations.AlterField(
                    model_name='item',
                    name='media_info',
                    field=models.JSONField(blank=True, db_column='media_info', default=irekua_database.utils.empty_JSON, help_text='Information of resource file', verbose_name='media info'),
                ),
                migrations.AlterField(
                    model_name='item',
                    name='metadata',
                    field=models.JSONField(blank=True, db_column='metadata', default=irekua_database.utils.empty_JSON, help_text='Metadata associated to item', null=True, verbose_name='metadata'),
                ),
                migrations.AlterField(
                    model_name='licence',
                    name='metadata',
                    field=models.JSONField(blank=True, db_column='metadata', default=irekua_database.utils.empty_JSON, help_text='Metadata associated with licence', null=True, verbose_name='metadata'),
                ),
                migrations.AlterField(
                    model_name='licencetype',
                    name='metadata_schema',
                    field=models.JSONField(blank=True, db_column='metadata_schema', default=irekua_database.utils.simple_JSON_schema, help_text='JSON Schema for metadata of licence info', validators=[irekua_database.utils.validate_JSON_schema], verbose_name='metadata schema'),
                ),
                migrations.AlterField(
                    model_name='locality',
                    name='metadata',
                    field=models.JSONField(blank=True, db_column='metadata', default=irekua_database.utils.empty_JSON, help_text='Metadata associated to locality', null=True, verbose_name='metadata'),
                ),
                migrations.AlterField(
                    model_name='localitytype',
                    name='metadata_schema',
                    field=models.JSONField(blank=True, db_column='metadata_schema', default=irekua_database.utils.simple_JSON_schema, help_text='JSON Schema for metadata of localities of this type', null=True, validators=[irekua_database.utils.validate_JSON_schema], verbose_name='metadata_schema'),
                ),
                migrations.AlterField(
                    model_name='mimetype',
                    name='media_info_schema',
                    field=models.JSONField(blank=True, db_column='media_info_schema', default=irekua_database.utils.simple_JSON_schema, help_text='JSON Schema for item type media info', validators=[irekua_database.utils.validate_JSON_schema], verbose_name='media info schema'),
                ),
                migrations.AlterField(
                    model_name='physicaldevice',
                    name='metadata',
                    field=models.JSONField(blank=True, db_column='metadata', default=irekua_database.utils.empty_JSON, help_text='Metadata associated to device', null=True, verbose_name='metadata'),
                ),
                migrations.AlterField(
                    model_name='samplingevent',
                    name='metadata',
                    field=models.JSONField(blank=True, db_column='metadata', default=irekua_database.utils.empty_JSON, help_text='Metadata associated to sampling event', null=True, verbose_name='metadata'),
                ),
                migrations.AlterField(
                    model_name='samplingeventdevice',
                    name='configuration',
                    field=models.JSONField(blank=True, db_column='configuration', default=irekua_database.utils.empty_JSON, help_text='Configuration on device through the sampling event', null=True, verbose_name='configuration'),
                ),
                migrations.AlterField(
                    model_name='samplingeventdevice',
                    name='metadata',
                    field=models.JSONField(blank=True, db_column='metadata', default=irekua_database.utils.empty_JSON, help_text='Metadata associated to sampling event device', null=True, verbose_name='metadata'),
                ),
                migrations.AlterField(
                    model_name='samplingeventtype',
                    name='metadata_schema',
                    field=models.JSONField(blank=True, db_column='metadata_schema', default=irekua_database.utils.simple_JSON_schema, help_text='JSON Schema for metadata of sampling event info', validators=[irekua_database.utils.validate_JSON_schema], verbose_name='metadata schema'),
                ),
                migrations.AlterField(
                    model_name='samplingeventtypedevicetype',
                    name='metadata_schema',
                    field=models.JSONField(blank=True, db_column='metadata_schema', default=irekua_database.utils.simple_JSON_schema, help_text='JSON schema for metadata associated to device in sampling event', validators=[irekua_database.utils.validate_JSON_schema], verbose_name='metadata schema'),
                ),
                migrations.AlterField(
                    model_name='secondaryitem',
                    name='media_info',
                    field=models.JSONField(blank=True, db_column='media_info', default=irekua_database.utils.empty_JSON, help_text='Media information of secondary item file', null=True, verbose_name='media info'),
                ),
                migrations.AlterField(
                    model_name='sitedescriptor',
                    name='metadata',
                    field=models.JSONField(blank=True, db_column='metadata', default=irekua_database.utils.empty_JSON, help_text='Metadata associated to term', null=True, verbose_name='metadata'),
                ),
                migrations.AlterField(
                    model_name='sitedescriptortype',
                    name='metadata_schema',
                    field=models.JSONField(blank=True, db_column='metadata_schema', default=irekua_database.utils.simple_JSON_schema, help_text='JSON Schema for metadata of descriptors of this type', null=True, validators=[irekua_database.utils.validate_JSON_schema], verbose_name='metadata_schema'),
                ),
                migrations.AlterField(
                    model_name='sitetype',
                    name='metadata_schema',
                    field=models.JSONField(blank=True, db_column='metadata_schema', default=irekua_database.utils.simple_JSON_schema, help_text='JSON Schema for metadata of site info', validators=[irekua_database.utils.validate_JSON_schema], verbose_name='metadata schema'),
                ),
                migrations.DeleteModel(
                    name='Entailment',
                ),
                migrations.DeleteModel(
                    name='EntailmentType',
                ),
                migrations.DeleteModel(
                    name='Synonym',
                ),
                migrations.DeleteModel(
                    name='SynonymSuggestion',
                ),
                migrations.DeleteModel(
                    name='Term',
                ),
                migrations.DeleteModel(
                    name='TermSuggestion',
                ),
                migrations.DeleteModel(
                    name='TermType',
                ),
            ],
            database_operations=[
                migrations.AlterModelTable(
                    name='Entailment',
                    table='irekua_terms_entailment',
                ),
                migrations.AlterModelTable(
                    name='EntailmentType',
                    table='irekua_terms_entailmenttype',
                ),
                migrations.AlterModelTable(
                    name='Synonym',
                    table='irekua_terms_synonym',
                ),
                migrations.AlterModelTable(
                    name='SynonymSuggestion',
                    table='irekua_terms_synonymsuggestion',
                ),
                migrations.AlterModelTable(
                    name='Term',
                    table='irekua_terms_term',
                ),
                migrations.AlterModelTable(
                    name='TermSuggestion',
                    table='irekua_terms_termsuggestion',
                ),
                migrations.AlterModelTable(
                    name='TermType',
                    table='irekua_terms_termtype',
                ),
            ],
        ),
    ]
