import cv2

from abc import ABC, abstractmethod

from image.utils import get_pixel_brightness


class Contrast(ABC):
    @abstractmethod
    def contrast(self, image: "Image") -> None: ...


class LinearRowsContrast(Contrast):
    def __init__(self) -> None:
        pass

    def contrast(self, image) -> None:
        pixels = image.get_pixels()
        pixels_copy = image.copy().get_pixels()
        for i in range(image.width):
            for j in range(image.height):
                prev_bright = get_pixel_brightness(pixels_copy[i, j - 1])
                current_bright = get_pixel_brightness(pixels_copy[i, j])
                g = int(abs(prev_bright - current_bright))
                pixels[i, j] = (g, g, g)


class CannyContrast(Contrast):
    def __init__(self, threshold1: int, threshold2: int) -> None:
        self.threshold1 = threshold1
        self.threshold2 = threshold2

    def contrast(self, image: "Image") -> None:
        a = cv2.Canny(image.get(), self.threshold1, self.threshold2)
        image.set(a)
