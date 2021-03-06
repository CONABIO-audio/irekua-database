import os
import importlib.util

from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_database.base import IrekuaModelBase

from irekua_items.models import MediaInfoType
from irekua_items.models import MimeType
from irekua_items.models import ItemType

from irekua_devices.models import DeviceType
from irekua_devices.models import Device


def _select_by_priority(options, item_type=None, device=None, device_type=None):
    extractors = []

    for extractor in options:
        item_type_specific = item_type in extractor.item_types.all()
        if extractor.item_types.count() and not item_type_specific:
            # If the extractor has listed some item_types but does not contain
            # the selected item_type then do not use this extractor
            continue

        device_type_specific = device_type in extractor.device_types.all()
        if extractor.device_types.count() and not device_type_specific:
            # If the extractor has listed some device_types but does not contain
            # the selected device_type then do not use this extractor
            continue

        device_specific = device in extractor.devices.all()
        print(device, extractor.devices.all(), device_specific)
        if extractor.devices.count() and not device_specific:
            # If the extractor has listed some devices but does not contain
            # the selected device then do not use this extractor
            continue

        if item_type_specific and device_specific:
            # Extractors that are made for the current item_type and device
            # have the hightest priority
            extractors.append((extractor, 0))
            continue

        if item_type_specific and device_type_specific:
            # Next in priority are the extractors made for the current
            # item_type and device_type
            extractors.append((extractor, 1))
            continue

        if item_type_specific:
            # Next are the extractors that were made for the current
            # item type
            extractors.append((extractor, 2))
            continue

        if device_specific:
            # Next the extractors that were made for the current device
            extractors.append((extractor, 3))
            continue

        if device_type_specific:
            # Next the extractors that were made for the current device type
            extractors.append((extractor, 4))
            continue

        # And finally all other extractors in the options
        extractors.append((extractor, 5))

    extractors_by_priority = sorted(extractors, key=lambda x: x[1])

    try:
        return extractors_by_priority[0][0]

    except IndexError:
        raise MediaInfoExtractor.DoesNotExist(
            "No adequate media info extractor was found"
        )


class MediaInfoExtractor(IrekuaModelBase):
    name = models.CharField(
        max_length=64,
        unique=True,
        null=False,
        blank=False,
        db_column="name",
        verbose_name=_("name"),
        help_text=_("Name of the media info extractor"),
    )

    mime_type = models.ForeignKey(
        MimeType,
        models.CASCADE,
        db_column="mime_type_id",
        verbose_name=_("mime type"),
        help_text=_("Mime type of files on which this extractor operates."),
    )

    media_info_type = models.ForeignKey(
        MediaInfoType,
        models.CASCADE,
        db_column="media_info_type_id",
        verbose_name=_("media info type"),
        help_text=_("Media info type that can be extracted by this extractor"),
    )

    item_types = models.ManyToManyField(
        ItemType,
        help_text=_(
            "If empty this extractor should work on any item type."
            "Otherwise list the item types on which this extractor"
            "works."
        ),
    )

    device_types = models.ManyToManyField(
        DeviceType,
        help_text=_(
            "If empty this extractor should work on any device type."
            "Otherwise list the device types on which this extractor"
            "works."
        ),
    )

    devices = models.ManyToManyField(
        Device,
        help_text=_(
            "If empty this extractor should work on any device."
            "Otherwise list the devices on which this extractor works."
        ),
    )

    python_file = models.FileField(
        upload_to="media_info_extractors/",
        db_column="python_file",
        verbose_name=_("python file"),
        help_text=_("Python file containing the media info extractor function"),
        blank=True,
        null=True,
    )

    javascript_file = models.FileField(
        upload_to="media_info_extractors/",
        db_column="javascript_file",
        verbose_name=_("javascript file"),
        help_text=_("Javascript file containing the media info extractor function"),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Media Info Extractor")

        verbose_name_plural = _("Media Info Extractors")

        ordering = ["-created_on"]

    @classmethod
    def get_python_extractor(
        cls,
        mime_type,
        item_type=None,
        device=None,
        device_type=None,
    ):

        if device is not None and device_type is None:
            if not isinstance(device, Device):
                device = Device.objects.get(pk=device)

            device_type = device.device_type

        if isinstance(device, Device):
            device = device.pk

        if isinstance(device_type, DeviceType):
            device_type = device_type.pk

        if isinstance(item_type, ItemType):
            item_type = item_type.pk

        if isinstance(mime_type, MimeType):
            mime_type = mime_type.pk

        possible_extractors = cls.objects.filter(
            mime_type=mime_type,
            python_file__isnull=False,
        ).prefetch_related(
            "device_types",
            "item_types",
            "devices",
        )

        return _select_by_priority(
            possible_extractors,
            item_type=item_type,
            device=device,
            device_type=device_type,
        )

    def __str__(self):
        return str(self.name)

    def load_extractor(self):
        name = self.python_file.name
        basename = os.path.basename(name)
        module_name = os.path.splitext(basename)[0]

        spec = importlib.util.spec_from_file_location(
            module_name, self.python_file.path
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module.extract

    def extract_media_info(self, fileobj):
        extractor = self.load_extractor()
        return extractor(fileobj)
