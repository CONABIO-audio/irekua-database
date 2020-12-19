import io

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


#  Size of thumbnail
SIZE = (500, 500)


def thumbnail_creator(item_file):
    image = Image.open(item_file)

    thumbnail = image.convert("RGB")
    thumbnail.thumbnail(SIZE, Image.ANTIALIAS)

    buffer = io.BytesIO()
    thumbnail.save(fp=buffer, format="JPEG")
    buffer.seek(0)

    return InMemoryUploadedFile(
        buffer,
        None,
        "thumbnail.jpg",
        "image/jpeg",
        buffer.getbuffer().nbytes,
        None,
    )
