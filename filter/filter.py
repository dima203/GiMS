import cv2

from abc import ABC, abstractmethod


class Filter(ABC):
    @abstractmethod
    def apply(self, image) -> None: ...


class CancelFilter(Filter):
    """Отмена"""
    def apply(self, image) -> None:
        pass


class MedianFilter(Filter):
    """Медианный двумерный фильтр"""
    def __init__(self) -> None:
        self.ksize = 7  # int(input('Введите размер окна (нечетный): '))

    def apply(self, image) -> None:
        image.set(cv2.medianBlur(image.get(), self.ksize))
