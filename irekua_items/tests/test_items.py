import pytest

from irekua_items.tests.fixtures.items import *


@pytest.mark.parametrize(
    "sample_rate",
    [11025, 22050, 44100, 48000, 96000, 192000, 352000],
)
@pytest.mark.parametrize("channels", [1, 2])
@pytest.mark.parametrize("duration", [0.1, 0.5, 1, 10])
@pytest.mark.parametrize("sample_width", [2, 4])
def test_wav_fixture(
    generate_random_wav,
    sample_rate,
    channels,
    duration,
    sample_width,
):
    import wave

    fp = generate_random_wav(
        sample_rate=sample_rate,
        duration=duration,
        sample_width=sample_width,
        channels=channels,
    )

    with wave.open(fp, "rb") as wav:
        assert wav.getnchannels() == channels
        assert wav.getframerate() == sample_rate
        assert wav.getsampwidth() == sample_width
        assert wav.getnframes() == int(duration * wav.getframerate())
