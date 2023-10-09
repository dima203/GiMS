from .base import Effect

from image.image import Image


class FlipHorizontalEffect(Effect):
    def __init__(self, image) -> None:
        self.__image = image

    def apply(self) -> None:
        pixels = self.__image.get_pixels()
        pixels_copy = self.__image.copy().get_pixels()
        for i in range(self.__image.width):
            for j in range(self.__image.height):
                pixels[i, j] = pixels_copy[self.__image.width-i-1, j]


class ChessEffect(Effect):
    def __init__(self, image) -> None:
        self.__image = image

    def apply(self) -> None:
        image = Image.open()
        N = int(input('Введите N: '))
        pixels = self.__image.get_pixels()
        add_pixels = image.get_pixels()
        current_start_zone = True
        current_zone = True
        current_height = 0
        for j in range(self.__image.height):
            current_width = 0
            for i in range(self.__image.width):
                if not current_zone:
                    pixels[i, j] = add_pixels[i, j]
                current_width += 1
                if current_width >= N:
                    current_width = 0
                    current_zone = not current_zone
            current_height += 1
            if current_height >= N:
                current_zone = not current_start_zone
                current_start_zone = not current_start_zone
                current_height = 0
