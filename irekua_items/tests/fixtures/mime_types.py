import pytest

from irekua_items.models import MimeType


@pytest.fixture
@pytest.mark.django_db
def mime_type_factory():
    def create_mime_type(mime_type, media_info_type=None):
        return MimeType.objects.create(
            mime_type=mime_type, media_info_type=media_info_type
        )

    return create_mime_type


@pytest.fixture
@pytest.mark.django_db
def audio_wav(mime_type_factory):
    return mime_type_factory("audio/x-wav")


@pytest.mark.django_db
def image_png(mime_type_factory):
    return mime_type_factory("image/png")


@pytest.mark.django_db
def image_jpeg(mime_type_factory):
    return mime_type_factory("image/jpeg")


@pytest.mark.django_db
def video_avi(mime_type_factory):
    return mime_type_factory("video/x-msvideo")
