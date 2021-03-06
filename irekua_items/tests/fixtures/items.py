import uuid
from io import BytesIO

import pytest
import numpy as np
from django.core.files.uploadedfile import UploadedFile


@pytest.fixture
def generate_random_wav():
    import wave

    def create_random_wav(sample_rate=44100, duration=1, sample_width=2, channels=1):
        if sample_width not in [2, 4]:
            raise NotImplementedError

        length = int(sample_rate * duration)
        shape = (channels, length)
        array = np.random.random(size=shape)

        exponent = 8 * sample_width - 1
        dtype = "<h" if sample_width == 2 else "<i"
        audio = (array * (2 ** exponent - 1)).astype(dtype)

        fp = BytesIO()

        with wave.open(fp, mode="wb") as wav:
            wav.setnchannels(channels)
            wav.setsampwidth(sample_width)
            wav.setframerate(sample_rate)
            wav.writeframes(audio.tobytes())

        fp.seek(0)

        return UploadedFile(
            file=fp,
            name=f"{uuid.uuid1()}.wav",
            content_type="audio/x-wav",
        )

    return create_random_wav


@pytest.fixture
def generate_random_python_file():
    def create_random_python_file():
        fp = BytesIO()
        fp.write('print("hello world")'.encode("utf-8"))
        fp.seek(0)

        return UploadedFile(
            file=fp,
            name=f"{uuid.uuid1()}.py",
            content_type="text/x-python",
        )

    return create_random_python_file
