import cv2

from abc import ABC, abstractmethod


class Filter(ABC):
    @abstractmethod
    def filter(self, image) -> None: ...


class MedianCrossFilter(Filter):
    def __init__(self, ksize: int = 5) -> None:
        self.ksize = ksize

    def filter(self, image) -> None:
        image.set(cv2.medianBlur(image.get(), self.ksize))
        # pixels = image.get_pixels()
        # for j in range(image.height - self.window_height):
        #     for i in range(image.width - self.window_width):
        #         filter_map = []
        #         for window_i in range(self.window_width):
        #             for window_j in range(self.window_height):
                #                 self.__window[window_i][window_j][0] = pixels[i + window_i, j + window_j]
        #         for window_i in range(self.window_width):
        #             filter_map.append(self.__window[window_i][self.cross_y])
        #         for window_j in range(self.window_height):
        #             if window_j == self.cross_y:
        #                 continue
        #             filter_map.append(self.__window[self.cross_x][window_j])
        #         result_color = []
        #         for color in range(3):
        #             filter_map.sort(key=lambda x: x[0][color] * x[1])
        #             result_color.append(filter_map[len(filter_map) // 2][0][color])
        #         pixels[i + self.cross_x, j + self.cross_y] = tuple(result_color)
