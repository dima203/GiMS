from PIL import Image as Img

from random import randint

from filter import MedianCrossFilter
from contrast import LinearRowsContrast
from .utils import get_pixel_brightness


class Image:
    base_images_dir = './images/'
    base_save_dir = './results/'

    def __init__(self, image: Img.Image = None, image_name: str = '') -> None:
        if image is None:
            self.__image = None
        else:
            self.__image = image.copy()
        if self.__image is not None:
            self.width = self.__image.width
            self.height = self.__image.height
            self.__pixels = self.__image.load()
        self.image_name = image_name

    def get_image_name(self) -> str:
        return self.image_name

    @staticmethod
    def open() -> "Image":
        """Открыть изображение"""
        file_name = input('Введите имя файла: ')
        if not file_name.startswith(('/', './', '~/')):
            file_name = Image.base_images_dir + file_name
        return Image(Img.open(file_name), file_name)

    def save(self) -> "Image":
        """Сохранить изображение"""
        if self.__image is None:
            print('Изображение не открыто')
            return self
        file_name = input('Введите имя файла: ')
        if not file_name.startswith(('/', './', '~/')):
            file_name = Image.base_save_dir + file_name
        self.__image.save(file_name)
        self.image_name = self.image_name if not self.image_name.endswith('*') else self.image_name[:-1]
        return self

    def show(self) -> "Image":
        """Просмотреть изображение"""
        if self.__image is None:
            print('Изображение не открыто')
            return self
        self.__image.show()
        return self

    def add_noise(self) -> "Image":
        """Добавить шум на изображение"""
        if self.__image is None:
            print('Изображение не открыто')
            return self
        probability = int(input('Введите вероятность шума: '))
        image = Image(self.__image, self.image_name+'*' if not self.image_name.endswith('*') else self.image_name)
        pixels = image.get_pixels()
        size = image.width * image.height
        count = (size * probability) // 100
        for i in range(count):
            x = randint(0, image.width - 1)
            y = randint(0, image.height - 1)
            pixels[x, y] = (randint(0, 255), randint(0, 255), randint(0, 255))
        return image

    def filter(self) -> "Image":
        """Отфильтровать изображение"""
        if self.__image is None:
            print('Изображение не открыто')
            return self
        window_width, window_height = map(int, input('Введите размер окна: ').split())
        cross_x, cross_y = map(int, input('Введите центр креста (начиная с 0): ').split())
        image_filter = MedianCrossFilter(window_width, window_height, cross_x, cross_y)
        image = Image(self.__image, self.image_name+'*' if not self.image_name.endswith('*') else self.image_name)
        image_filter.input_window()
        image_filter.filter(image)
        return image

    def contrast(self) -> "Image":
        """Получить контрастное изображение"""
        if self.__image is None:
            print('Изображение не открыто')
            return self
        image_contrast = LinearRowsContrast()
        image = Image(self.__image, self.image_name + '*' if not self.image_name.endswith('*') else self.image_name)
        image_contrast.contrast(image)
        return image

    def get_edge_image(self) -> "Image":
        """Получить контур изображения"""
        if self.__image is None:
            print('Изображение не открыто')
            return self
        image = Image(self.__image, self.image_name + '*' if not self.image_name.endswith('*') else self.image_name)
        pixels = image.get_pixels()
        e = image._get_threshold()
        for i in range(image.width):
            for j in range(image.height):
                pixels[i, j] = (0, 0, 0) if get_pixel_brightness(pixels[i, j]) > e else (255, 255, 255)
        return image

    def get_pixels(self):
        return self.__pixels

    def copy(self) -> "Image":
        return Image(self.__image, self.image_name)

    def _get_threshold(self) -> int:
        pixels = self.get_pixels()
        brightness_map = [0 for _ in range(256)]
        pixels_count = self.width * self.height
        for i in range(self.width):
            for j in range(self.height):
                brightness_map[get_pixel_brightness(pixels[i, j])] += 1
        brightness_map = list(map(lambda x: x / pixels_count, brightness_map))
        threshold_percent = 0
        for i, brightness_rate in enumerate(brightness_map):
            threshold_percent += brightness_rate
            if threshold_percent >= 0.8:
                return i
