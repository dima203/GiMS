import numpy


def get_pixel_brightness(pixel: tuple[int] | numpy.uint8) -> int:
    if isinstance(pixel, numpy.uint8):
        return int(pixel)
    else:
        return int(pixel[0] * 0.33 + pixel[1] * 0.51 + pixel[2] * 0.16)
