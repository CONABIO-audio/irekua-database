# Generated by Django 3.1 on 2020-10-13 00:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('irekua_types', '0001_initial'),
        ('irekua_devices', '0001_initial'),
        ('irekua_items', '0001_initial'),
        ('irekua_geo', '0001_initial'),
        ('irekua_collections', '0001_initial'),
        ('irekua_database', '0013_change_item_to_deployment'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(
                    model_name='annotationvote',
                    name='annotation',
                ),
                migrations.RemoveField(
                    model_name='annotationvote',
                    name='created_by',
                ),
                migrations.RemoveField(
                    model_name='annotationvote',
                    name='labels',
                ),
                migrations.RemoveField(
                    model_name='annotationvote',
                    name='modified_by',
                ),
                migrations.RemoveField(
                    model_name='collection',
                    name='administrators',
                ),
                migrations.RemoveField(
                    model_name='collection',
                    name='collection_type',
                ),
                migrations.RemoveField(
                    model_name='collection',
                    name='created_by',
                ),
                migrations.RemoveField(
                    model_name='collection',
                    name='institution',
                ),
                migrations.RemoveField(
                    model_name='collection',
                    name='modified_by',
                ),
                migrations.RemoveField(
                    model_name='collection',
                    name='physical_devices',
                ),
                migrations.RemoveField(
                    model_name='collection',
                    name='sites',
                ),
                migrations.RemoveField(
                    model_name='collection',
                    name='users',
                ),
                migrations.AlterUniqueTogether(
                    name='collectiondevice',
                    unique_together=None,
                ),
                migrations.RemoveField(
                    model_name='collectiondevice',
                    name='collection',
                ),
                migrations.RemoveField(
                    model_name='collectiondevice',
                    name='created_by',
                ),
                migrations.RemoveField(
                    model_name='collectiondevice',
                    name='modified_by',
                ),
                migrations.RemoveField(
                    model_name='collectiondevice',
                    name='physical_device',
                ),
                migrations.AlterUniqueTogether(
                    name='collectiondevicetype',
                    unique_together=None,
                ),
                migrations.RemoveField(
                    model_name='collectiondevicetype',
                    name='collection_type',
                ),
                migrations.RemoveField(
                    model_name='collectiondevicetype',
                    name='device_type',
                ),
                migrations.RemoveField(
                    model_name='collectionitem',
                    name='collection',
                ),
                migrations.RemoveField(
                    model_name='collectionitem',
                    name='item_ptr',
                ),
                migrations.AlterUniqueTogether(
                    name='collectionitemtype',
                    unique_together=None,
                ),
                migrations.RemoveField(
                    model_name='collectionitemtype',
                    name='collection_type',
                ),
                migrations.RemoveField(
                    model_name='collectionitemtype',
                    name='item_type',
                ),
                migrations.RemoveField(
                    model_name='collectionlicence',
                    name='collection',
                ),
                migrations.RemoveField(
                    model_name='collectionlicence',
                    name='licence_ptr',
                ),
                migrations.AlterUniqueTogether(
                    name='collectionrole',
                    unique_together=None,
                ),
                migrations.RemoveField(
                    model_name='collectionrole',
                    name='collection_type',
                ),
                migrations.RemoveField(
                    model_name='collectionrole',
                    name='role',
                ),
                migrations.AlterUniqueTogether(
                    name='collectionsite',
                    unique_together=None,
                ),
                migrations.RemoveField(
                    model_name='collectionsite',
                    name='collection',
                ),
                migrations.RemoveField(
                    model_name='collectionsite',
                    name='created_by',
                ),
                migrations.RemoveField(
                    model_name='collectionsite',
                    name='modified_by',
                ),
                migrations.RemoveField(
                    model_name='collectionsite',
                    name='site',
                ),
                migrations.RemoveField(
                    model_name='collectionsite',
                    name='site_descriptors',
                ),
                migrations.RemoveField(
                    model_name='collectionsite',
                    name='site_type',
                ),
                migrations.RemoveField(
                    model_name='collectiontype',
                    name='administrators',
                ),
                migrations.RemoveField(
                    model_name='collectiontype',
                    name='annotation_types',
                ),
                migrations.RemoveField(
                    model_name='collectiontype',
                    name='device_types',
                ),
                migrations.RemoveField(
                    model_name='collectiontype',
                    name='event_types',
                ),
                migrations.RemoveField(
                    model_name='collectiontype',
                    name='item_types',
                ),
                migrations.RemoveField(
                    model_name='collectiontype',
                    name='licence_types',
                ),
                migrations.RemoveField(
                    model_name='collectiontype',
                    name='roles',
                ),
                migrations.RemoveField(
                    model_name='collectiontype',
                    name='sampling_event_types',
                ),
                migrations.RemoveField(
                    model_name='collectiontype',
                    name='site_types',
                ),
                migrations.AlterUniqueTogether(
                    name='collectionuser',
                    unique_together=None,
                ),
                migrations.RemoveField(
                    model_name='collectionuser',
                    name='collection',
                ),
                migrations.RemoveField(
                    model_name='collectionuser',
                    name='created_by',
                ),
                migrations.RemoveField(
                    model_name='collectionuser',
                    name='modified_by',
                ),
                migrations.RemoveField(
                    model_name='collectionuser',
                    name='role',
                ),
                migrations.RemoveField(
                    model_name='collectionuser',
                    name='user',
                ),
                migrations.AlterUniqueTogether(
                    name='deployment',
                    unique_together=None,
                ),
                migrations.RemoveField(
                    model_name='deployment',
                    name='collection_device',
                ),
                migrations.RemoveField(
                    model_name='deployment',
                    name='created_by',
                ),
                migrations.RemoveField(
                    model_name='deployment',
                    name='deployment_type',
                ),
                migrations.RemoveField(
                    model_name='deployment',
                    name='licence',
                ),
                migrations.RemoveField(
                    model_name='deployment',
                    name='modified_by',
                ),
                migrations.RemoveField(
                    model_name='deployment',
                    name='sampling_event',
                ),
                migrations.RemoveField(
                    model_name='deploymentitem',
                    name='deployment',
                ),
                migrations.RemoveField(
                    model_name='deploymentitem',
                    name='samplingeventitem_ptr',
                ),
                migrations.RemoveField(
                    model_name='deploymenttype',
                    name='device_type',
                ),
                migrations.AlterUniqueTogether(
                    name='device',
                    unique_together=None,
                ),
                migrations.RemoveField(
                    model_name='device',
                    name='brand',
                ),
                migrations.RemoveField(
                    model_name='device',
                    name='device_type',
                ),
                migrations.RemoveField(
                    model_name='devicetype',
                    name='mime_types',
                ),
                migrations.RemoveField(
                    model_name='eventtype',
                    name='should_imply',
                ),
                migrations.RemoveField(
                    model_name='eventtype',
                    name='term_types',
                ),
                migrations.RemoveField(
                    model_name='item',
                    name='created_by',
                ),
                migrations.RemoveField(
                    model_name='item',
                    name='item_type',
                ),
                migrations.RemoveField(
                    model_name='item',
                    name='licence',
                ),
                migrations.RemoveField(
                    model_name='item',
                    name='modified_by',
                ),
                migrations.RemoveField(
                    model_name='item',
                    name='ready_event_types',
                ),
                migrations.RemoveField(
                    model_name='item',
                    name='source',
                ),
                migrations.RemoveField(
                    model_name='item',
                    name='tags',
                ),
                migrations.RemoveField(
                    model_name='itemthumbnail',
                    name='item',
                ),
                migrations.RemoveField(
                    model_name='itemtype',
                    name='event_types',
                ),
                migrations.RemoveField(
                    model_name='itemtype',
                    name='mime_types',
                ),
                migrations.RemoveField(
                    model_name='licence',
                    name='created_by',
                ),
                migrations.RemoveField(
                    model_name='licence',
                    name='licence_type',
                ),
                migrations.RemoveField(
                    model_name='licence',
                    name='modified_by',
                ),
                migrations.RemoveField(
                    model_name='locality',
                    name='is_part_of',
                ),
                migrations.RemoveField(
                    model_name='locality',
                    name='locality_type',
                ),
                migrations.RemoveField(
                    model_name='metacollection',
                    name='created_by',
                ),
                migrations.RemoveField(
                    model_name='metacollection',
                    name='curators',
                ),
                migrations.RemoveField(
                    model_name='metacollection',
                    name='items',
                ),
                migrations.RemoveField(
                    model_name='metacollection',
                    name='modified_by',
                ),
                migrations.AlterUniqueTogether(
                    name='physicaldevice',
                    unique_together=None,
                ),
                migrations.RemoveField(
                    model_name='physicaldevice',
                    name='created_by',
                ),
                migrations.RemoveField(
                    model_name='physicaldevice',
                    name='device',
                ),
                migrations.RemoveField(
                    model_name='physicaldevice',
                    name='modified_by',
                ),
                migrations.RemoveField(
                    model_name='samplingevent',
                    name='collection',
                ),
                migrations.RemoveField(
                    model_name='samplingevent',
                    name='collection_site',
                ),
                migrations.RemoveField(
                    model_name='samplingevent',
                    name='created_by',
                ),
                migrations.RemoveField(
                    model_name='samplingevent',
                    name='licence',
                ),
                migrations.RemoveField(
                    model_name='samplingevent',
                    name='modified_by',
                ),
                migrations.RemoveField(
                    model_name='samplingevent',
                    name='sampling_event_type',
                ),
                migrations.RemoveField(
                    model_name='samplingeventitem',
                    name='collectionitem_ptr',
                ),
                migrations.RemoveField(
                    model_name='samplingeventitem',
                    name='sampling_event',
                ),
                migrations.RemoveField(
                    model_name='samplingeventtype',
                    name='deployment_types',
                ),
                migrations.RemoveField(
                    model_name='samplingeventtype',
                    name='site_types',
                ),
                migrations.RemoveField(
                    model_name='secondaryitem',
                    name='item',
                ),
                migrations.RemoveField(
                    model_name='secondaryitem',
                    name='item_type',
                ),
                migrations.RemoveField(
                    model_name='site',
                    name='created_by',
                ),
                migrations.RemoveField(
                    model_name='site',
                    name='locality',
                ),
                migrations.RemoveField(
                    model_name='site',
                    name='modified_by',
                ),
                migrations.AlterUniqueTogether(
                    name='sitedescriptor',
                    unique_together=None,
                ),
                migrations.RemoveField(
                    model_name='sitedescriptor',
                    name='descriptor_type',
                ),
                migrations.RemoveField(
                    model_name='sitetype',
                    name='site_descriptor_types',
                ),
                migrations.RemoveField(
                    model_name='source',
                    name='uploader',
                ),
                migrations.DeleteModel(
                    name='Annotation',
                ),
                migrations.DeleteModel(
                    name='AnnotationType',
                ),
                migrations.DeleteModel(
                    name='AnnotationVote',
                ),
                migrations.DeleteModel(
                    name='Collection',
                ),
                migrations.DeleteModel(
                    name='CollectionDevice',
                ),
                migrations.DeleteModel(
                    name='CollectionDeviceType',
                ),
                migrations.DeleteModel(
                    name='CollectionItem',
                ),
                migrations.DeleteModel(
                    name='CollectionItemType',
                ),
                migrations.DeleteModel(
                    name='CollectionLicence',
                ),
                migrations.DeleteModel(
                    name='CollectionRole',
                ),
                migrations.DeleteModel(
                    name='CollectionSite',
                ),
                migrations.DeleteModel(
                    name='CollectionType',
                ),
                migrations.DeleteModel(
                    name='CollectionUser',
                ),
                migrations.DeleteModel(
                    name='Deployment',
                ),
                migrations.DeleteModel(
                    name='DeploymentItem',
                ),
                migrations.DeleteModel(
                    name='DeploymentType',
                ),
                migrations.DeleteModel(
                    name='Device',
                ),
                migrations.DeleteModel(
                    name='DeviceBrand',
                ),
                migrations.DeleteModel(
                    name='DeviceType',
                ),
                migrations.DeleteModel(
                    name='EventType',
                ),
                migrations.DeleteModel(
                    name='Item',
                ),
                migrations.DeleteModel(
                    name='ItemThumbnail',
                ),
                migrations.DeleteModel(
                    name='ItemType',
                ),
                migrations.DeleteModel(
                    name='Licence',
                ),
                migrations.DeleteModel(
                    name='LicenceType',
                ),
                migrations.DeleteModel(
                    name='Locality',
                ),
                migrations.DeleteModel(
                    name='LocalityType',
                ),
                migrations.DeleteModel(
                    name='MetaCollection',
                ),
                migrations.DeleteModel(
                    name='MimeType',
                ),
                migrations.DeleteModel(
                    name='PhysicalDevice',
                ),
                migrations.DeleteModel(
                    name='SamplingEvent',
                ),
                migrations.DeleteModel(
                    name='SamplingEventItem',
                ),
                migrations.DeleteModel(
                    name='SamplingEventType',
                ),
                migrations.DeleteModel(
                    name='SecondaryItem',
                ),
                migrations.DeleteModel(
                    name='Site',
                ),
                migrations.DeleteModel(
                    name='SiteDescriptor',
                ),
                migrations.DeleteModel(
                    name='SiteDescriptorType',
                ),
                migrations.DeleteModel(
                    name='SiteType',
                ),
                migrations.DeleteModel(
                    name='Source',
                ),
                migrations.DeleteModel(
                    name='Tag',
                ),
            ],
            database_operations=[
                migrations.AlterModelTable(
                    name='Annotation',
                    table='irekua_items_annotation',
                ),
                migrations.AlterModelTable(
                    name='AnnotationType',
                    table='irekua_types_annotationtype',
                ),
                migrations.AlterModelTable(
                    name='AnnotationVote',
                    table='irekua_items_annotationvote',
                ),
                migrations.AlterModelTable(
                    name='Collection',
                    table='irekua_collections_collection',
                ),
                migrations.AlterModelTable(
                    name='CollectionDevice',
                    table='irekua_collections_collectiondevice',
                ),
                migrations.AlterModelTable(
                    name='CollectionDeviceType',
                    table='irekua_collections_collectiondevicetype',
                ),
                migrations.AlterModelTable(
                    name='CollectionItem',
                    table='irekua_collections_collectionitem',
                ),
                migrations.AlterModelTable(
                    name='CollectionItemType',
                    table='irekua_collections_collectionitemtype',
                ),
                migrations.AlterModelTable(
                    name='CollectionLicence',
                    table='irekua_collections_collectionlicence',
                ),
                migrations.AlterModelTable(
                    name='CollectionRole',
                    table='irekua_collections_collectionrole',
                ),
                migrations.AlterModelTable(
                    name='CollectionSite',
                    table='irekua_collections_collectionsite',
                ),
                migrations.AlterModelTable(
                    name='CollectionType',
                    table='irekua_collections_collectiontype',
                ),
                migrations.AlterModelTable(
                    name='CollectionUser',
                    table='irekua_collections_collectionuser',
                ),
                migrations.AlterModelTable(
                    name='CollectionUser',
                    table='irekua_collections_collectionuser',
                ),
                migrations.AlterModelTable(
                    name='Deployment',
                    table='irekua_collections_deployment',
                ),
                migrations.AlterModelTable(
                    name='DeploymentItem',
                    table='irekua_collections_deploymentitem',
                ),
                migrations.AlterModelTable(
                    name='DeploymentType',
                    table='irekua_types_deploymenttype',
                ),
                migrations.AlterModelTable(
                    name='Device',
                    table='irekua_devices_device',
                ),
                migrations.AlterModelTable(
                    name='DeviceBrand',
                    table='irekua_devices_devicebrand',
                ),
                migrations.AlterModelTable(
                    name='DeviceType',
                    table='irekua_types_devicetype',
                ),
                migrations.AlterModelTable(
                    name='EventType',
                    table='irekua_types_eventtype',
                ),
                migrations.AlterModelTable(
                    name='Item',
                    table='irekua_items_item',
                ),
                migrations.AlterModelTable(
                    name='ItemThumbnail',
                    table='irekua_items_itemthumbnail',
                ),
                migrations.AlterModelTable(
                    name='ItemType',
                    table='irekua_types_itemtype',
                ),
                migrations.AlterModelTable(
                    name='Licence',
                    table='irekua_items_licence',
                ),
                migrations.AlterModelTable(
                    name='LicenceType',
                    table='irekua_types_licencetype',
                ),
                migrations.AlterModelTable(
                    name='LicenceType',
                    table='irekua_types_licencetype',
                ),
                migrations.AlterModelTable(
                    name='Locality',
                    table='irekua_geo_locality',
                ),
                migrations.AlterModelTable(
                    name='LocalityType',
                    table='irekua_types_localitytype',
                ),
                migrations.AlterModelTable(
                    name='MimeType',
                    table='irekua_types_mimetype',
                ),
                migrations.AlterModelTable(
                    name='PhysicalDevice',
                    table='irekua_devices_physicaldevice',
                ),
                migrations.AlterModelTable(
                    name='SamplingEvent',
                    table='irekua_collections_samplingevent',
                ),
                migrations.AlterModelTable(
                    name='SamplingEventItem',
                    table='irekua_collections_samplingeventitem',
                ),
                migrations.AlterModelTable(
                    name='SamplingEventType',
                    table='irekua_types_samplingeventtype',
                ),
                migrations.AlterModelTable(
                    name='SecondaryItem',
                    table='irekua_items_secondaryitem',
                ),
                migrations.AlterModelTable(
                    name='Site',
                    table='irekua_geo_site',
                ),
                migrations.AlterModelTable(
                    name='SiteDescriptor',
                    table='irekua_geo_sitedescriptor',
                ),
                migrations.AlterModelTable(
                    name='SiteDescriptorType',
                    table='irekua_types_sitedescriptortype',
                ),
                migrations.AlterModelTable(
                    name='SiteType',
                    table='irekua_types_sitetype',
                ),
                migrations.AlterModelTable(
                    name='Source',
                    table='irekua_items_source',
                ),
                migrations.AlterModelTable(
                    name='Tag',
                    table='irekua_items_tag',
                ),
            ],
        ),
    ]
