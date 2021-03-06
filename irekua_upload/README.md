# Irekua Items


## Media Info and Inferable Metadata

### Introduction

For specific item types it might be possible, and desirable, to
automatically extract the media info and some additional metadata from
the file itself. This has to be done on a per item type/mime type/device
basis since the structure of the expected data can vary depending on file
format, capturing device and nature of such file. Additionally, this
automated extraction might not be suitable for all types of collections,
since for some cases it might be preferable to let the user fill out the
metadata information.

In order to add flexibility to Irekua's file handling we have included a
way of registering media info and metadata extractors for specific item
type/mime type/device/collection type combinations.

### Extractors

A extractor can be of two types: MediaInfoExtractor and MetadataExtractor.


#### Media Info Extractors

These stored functions can read a file and return the contained
media info. Most file formats have a relatively uniform media info
structure which, in some cases, can be expanded with additional
information.

```python
class MediaInfoExtractor(Model):
    mime_type = ForeignKey(MimeType, blank=False, null=False)
    media_info_type = ForeingKey(MediaInfoType, blank=False,
    null=False)

    item_types = ManyToMany(ItemType)
    device_types = ManyToMany(DeviceType)
    devices = ManyToMany(Device)

    python_file = FileField()
    javascript_file = FileField()

    class Meta:
        unique_together = (
            (mime_type, item_type, device_type, device),
        )
```


```python
def get_python_extractor(item_type, mime_type, device):
    possible_extractors = (
        MediaInfoExtractor
        .objects
        .filter(
            mime_type=mime_type,
            python_file__isnull=False
        )
    )

    device_type = device.device_type

    extractors = []
    for extractor in possible_extractors:
        item_type_specific = item_type.pk in extractor.item_types
        if extractor.item_types and not item_type_specific:
            continue

        device_type_specific = device_type.pk in extractor.device_types
        if extractor.device_types and not device_type_specific:
            continue

        device_specific = device.pk in extractor.devices
        if extractor.devices and not device_specific:
            continue

        if item_type_specific and device_specific:
            extractors.append((extractor, 0))
            continue

        if item_type_specific and device_type_specific:
            extractors.append((extractor, 1))
            continue

        if item_type_specific:
            extractors.append((extractor, 2))
            continue

        if device_specific:
            extractors.append((extractor, 3))
            continue

        if device_type_specific:
            extractors.append((extractor, 4))
            continue

        extractors.append((extractor, 5))

    extractors_by_priority = sorted(extractors, key=lambda x: x[1])
    return extractors_by_priority[0][0]

```



### Extractor selection
