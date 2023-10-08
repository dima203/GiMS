def get_pixel_brightness(pixel: tuple[int]) -> int:
    return int(pixel[0] * 0.33 + pixel[1] * 0.5 + pixel[2] * 0.16)
