import cv2
from numpy import asarray, float32

from abc import ABC, abstractmethod

import imglib.image


class Effect(ABC):
    @abstractmethod
    def apply(self, image) -> None: ...


class CancelEffect(Effect):
    """Отмена"""
    def apply(self, image) -> None:
        pass


class FlipHorizontalEffect(Effect):
    """Переворот по горизонтали"""
    def apply(self, image) -> None:
        pixels = image.get()
        src = asarray([[0, 0], [image.width - 1, 0], [0, image.height - 1]], dtype=float32)
        dst = asarray([[image.width - 1, 0], [0, 0], [image.width - 1, image.height - 1]], dtype=float32)
        matrix = cv2.getAffineTransform(src, dst)
        image.set(cv2.warpAffine(pixels, matrix, [image.width, image.height]))


class FlipVerticalEffect(Effect):
    """Переворот по вертикали"""
    def apply(self, image) -> None:
        pixels = image.get()
        src = asarray([[0, 0], [image.width - 1, 0], [0, image.height - 1]], dtype=float32)
        dst = asarray([[0, image.height - 1], [image.width - 1, image.height - 1], [0, 0]], dtype=float32)
        matrix = cv2.getAffineTransform(src, dst)
        image.set(cv2.warpAffine(pixels, matrix, [image.width, image.height]))


class ChessEffect(Effect):
    """Смешение изображений в шахматном порядке"""
    def __init__(self) -> None:
        self.image = imglib.image.Image.open()
        self.N = int(input('Введите N: '))

    def apply(self, image) -> None:
        pixels = image.get()
        add_pixels = self.image.get()
        current_start_zone = True
        current_zone = True
        current_height = 0
        for j in range(image.height):
            current_width = 0
            for i in range(image.width):
                if not current_zone:
                    pixels[j, i] = add_pixels[j, i]
                current_width += 1
                if current_width >= self.N:
                    current_width = 0
                    current_zone = not current_zone
            current_height += 1
            if current_height >= self.N:
                current_zone = not current_start_zone
                current_start_zone = not current_start_zone
                current_height = 0
