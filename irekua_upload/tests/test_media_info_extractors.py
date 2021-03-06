import pytest
from pytest_django.asserts import assertNumQueries

from irekua_upload.models import MediaInfoExtractor

from irekua_items.tests.fixtures.item_types import *
from irekua_items.tests.fixtures.mime_types import *

from irekua_devices.tests.fixtures.device_types import *
from irekua_devices.tests.fixtures.devices import *

from irekua_upload.tests.fixtures.media_info_extractors import *


@pytest.mark.django_db
def test_get_python_extractor(
    media_info_extractor_factory,
    item_type_A,
    item_type_B,
    camera,
    recorder,
    camera_A,
    recorder_A,
    audio_wav,
    image_png,
):
    get_extractor = MediaInfoExtractor.get_python_extractor

    with pytest.raises(MediaInfoExtractor.DoesNotExist):
        get_extractor(mime_type=audio_wav)

    extractor1 = media_info_extractor_factory("extractor 1", audio_wav)

    assert get_extractor(mime_type=audio_wav) == extractor1

    extractor2 = media_info_extractor_factory(
        "extractor 2",
        audio_wav,
        devices=[recorder_A],
    )

    assert get_extractor(mime_type=audio_wav) == extractor1
    assert get_extractor(mime_type=audio_wav, device=recorder_A) == extractor2
