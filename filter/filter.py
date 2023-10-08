from abc import ABC, abstractmethod


class Filter(ABC):
    @abstractmethod
    def filter(self, image: "Image") -> None: ...


class MedianCrossFilter(Filter):
    def __init__(self, window_width: int, window_height: int, cross_x: int, cross_y: int) -> None:
        self.window_width = window_width
        self.window_height = window_height
        self.cross_x = cross_x
        self.cross_y = cross_y
        self.__window = [
            [[(), 0] for _ in range(window_width)] for _ in range(window_height)
        ]

    def input_window(self) -> None:
        for i in range(self.window_height):
            for j in range(self.window_width):
                print('\n======================')
                self._print_weights(i, j)
                if j == self.cross_x or i == self.cross_y:
                    self.__window[i][j][1] = int(input())
        print('\n======================')
        self._print_weights()

    def filter(self, image) -> None:
        pixels = image.get_pixels()
        for j in range(image.height - self.window_height):
            for i in range(image.width - self.window_width):
                filter_map = []
                for window_i in range(self.window_width):
                    for window_j in range(self.window_height):
                        self.__window[window_i][window_j][0] = pixels[i + window_i, j + window_j]
                for window_i in range(self.window_width):
                    filter_map.append(self.__window[window_i][self.cross_y])
                for window_j in range(self.window_height):
                    if window_j == self.cross_y:
                        continue
                    filter_map.append(self.__window[self.cross_x][window_j])
                result_color = []
                for color in range(3):
                    filter_map.sort(key=lambda x: x[0][color] * x[1])
                    result_color.append(filter_map[len(filter_map) // 2][0][color])
                pixels[i + self.cross_x, j + self.cross_y] = tuple(result_color)

    def _print_weights(self, current_i: int = -1, current_j: int = -1):
        is_stopped = False
        for i in range(self.window_height):
            for j in range(self.window_width):
                if current_i == i and current_j == j:
                    is_stopped = True
                    break
                print(f'{self.__window[i][j][1]} ', end='')
            if is_stopped:
                break
            print()
