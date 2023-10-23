import cv2

from abc import ABC, abstractmethod

from imglib.utils import get_pixel_brightness


class Contrast(ABC):
    @abstractmethod
    def apply(self, image) -> None: ...


class CancelContrast(Contrast):
    """Отмена"""

    def __init__(self):
        pass

    def apply(self, image) -> None:
        pass


class LinearRowsContrast(Contrast):
    """Метод разностей по столбцам"""
    def __init__(self) -> None:
        pass

    def apply(self, image) -> None:
        pixels = image.get()
        pixels_copy = image.copy().get()
        for i in range(image.height):
            for j in range(image.width):
                prev_bright = get_pixel_brightness(pixels_copy[i, j - 1])
                current_bright = get_pixel_brightness(pixels_copy[i, j])
                g = int(abs(prev_bright - current_bright))
                pixels[i, j] = (g, g, g)


class CannyContrast(Contrast):
    """Фильтр Кенни"""
    def __init__(self) -> None:
        self.threshold1 = 100  # int(input('Введите нижний порог: '))
        self.threshold2 = 200  # int(input('Введите верхний порог: '))

    def apply(self, image) -> None:
        a = cv2.Canny(image.get(), self.threshold1, self.threshold2)
        image.set(cv2.cvtColor(a, cv2.COLOR_GRAY2RGB))
