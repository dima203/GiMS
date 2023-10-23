import cv2
from numpy import asarray, float32

from abc import ABC, abstractmethod


class Effect(ABC):
    @abstractmethod
    def apply(self) -> None: ...


class FlipHorizontalEffect(Effect):
    def __init__(self, image) -> None:
        self.__image = image

    def apply(self) -> None:
        pixels = self.__image.get_pixels()
        pixels_copy = self.__image.copy().get_pixels()
        for i in range(self.__image.width):
            for j in range(self.__image.height):
                pixels[i, j] = pixels_copy[self.__image.width-i-1, j]


class FlipVerticalEffect(Effect):
    def __init__(self, image) -> None:
        self.__image = image

    def apply(self) -> None:
        pixels = self.__image.get()
        src = asarray([[0, 0], [pixels.shape[0] - 1, 0], [0, pixels.shape[1] - 1]], dtype=float32)
        dst = asarray([[0, pixels.shape[1] - 1], [pixels.shape[0] - 1, pixels.shape[1] - 1], [0, 0]], dtype=float32)
        matrix = cv2.getAffineTransform(src, dst)
        self.__image.set(cv2.warpAffine(pixels, matrix, [pixels.shape[0], pixels.shape[1]]))


class ChessEffect(Effect):
    def __init__(self, image) -> None:
        self.__image = image

    def apply(self) -> None:
        # image = Image.open()
        N = int(input('Введите N: '))
        pixels = self.__image.get_pixels()
        add_pixels = self.__image.get_pixels()
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
