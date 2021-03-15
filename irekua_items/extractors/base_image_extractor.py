from PIL import Image


def extract(fileobj):
    try:
        im = Image.open(fileobj)

    except Exception as error:
        return None

    return {
        "Format": im.format,
        "Width": im.width,
        "Height": im.height,
        "BitDepth": im.bits,
        "Layers": im.layers,
        "Mode": im.mode,
    }
