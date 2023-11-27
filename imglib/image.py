import cv2
import numpy

from random import randint

from filter import Filter
from contrast import Contrast
from effect import Effect
from .utils import get_pixel_brightness


class Image:
    base_images_dir = './images/'
    base_save_dir = './results/'

    def __init__(self, image=None, image_name: str = '') -> None:
        if image is None:
            self.__is_none_image = True
            self.__image = numpy.zeros((500, 500))
            self.height, self.width = 500, 500
        else:
            self.__is_none_image = False
            self.__image = image.copy()
            self.height, self.width, *_ = self.__image.shape
        self.image_name = image_name

    def get_image_name(self) -> str:
        return self.image_name

    @staticmethod
    def open(path: str = None) -> "Image":
        """Открыть изображение"""
        if path is None:
            path = input('Введите имя файла: ')
            if not path.startswith(('/', './', '~/')):
                path = Image.base_images_dir + path
        return Image(cv2.imread(path), path)

    def save(self, path: str = None) -> "Image":
        """Сохранить изображение"""
        if self.__is_none_image:
            print('Изображение не открыто')
            return self

        if path is None:
            path = input('Введите имя файла: ')
            if not path.startswith(('/', './', '~/')):
                path = Image.base_save_dir + path
        cv2.imwrite(path, self.__image)
        self.image_name = self.image_name if not self.image_name.endswith('*') else self.image_name[:-1]
        return self

    def show(self) -> "Image":
        """Просмотреть изображение"""
        if self.__is_none_image:
            print('Изображение не открыто')
            return self

        cv2.imshow(self.image_name, self.__image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return self

    def add_noise(self, noise_amount: int = None) -> "Image":
        """Добавить шум на изображение"""
        if self.__is_none_image:
            print('Изображение не открыто')
            return self

        if noise_amount is None:
            noise_amount = int(input('Введите вероятность шума: '))
        image = Image(self.__image, self.image_name+'*' if not self.image_name.endswith('*') else self.image_name)
        pixels = image.get()
        size = image.width * image.height
        count = (size * noise_amount) // 100
        for _ in range(count):
            x = randint(0, image.width - 1)
            y = randint(0, image.height - 1)
            pixels[y, x] = (randint(0, 255), randint(0, 255), randint(0, 255))
        return image

    def filter(self, filter_number: str = None) -> "Image":
        """Отфильтровать изображение"""
        if self.__is_none_image:
            print('Изображение не открыто')
            return self

        return self._apply_action(Filter, filter_number)

    def contrast(self, contrast_number: str = None) -> "Image":
        """Получить контрастное изображение"""
        if self.__is_none_image:
            print('Изображение не открыто')
            return self

        return self._apply_action(Contrast, contrast_number)

    def get_edge(self, threshold: int = None) -> "Image":
        """Получить контур изображения"""
        if self.__is_none_image:
            print('Изображение не открыто')
            return self

        image = Image(self.__image, self.image_name + '*' if not self.image_name.endswith('*') else self.image_name)
        pixels = image.get()
        if threshold is None:
            threshold = int(input('Введите порог отсечения по гистограмме: '))
        e = image._get_threshold(threshold)
        for i in range(image.height):
            for j in range(image.width):
                pixels[i, j] = 0 if get_pixel_brightness(pixels[i, j]) > e else 255
        return image

    def effect(self, effect_number: str = None) -> "Image":
        """Применить эффект"""
        if self.__is_none_image:
            print('Изображение не открыто')
            return self

        return self._apply_action(Effect, effect_number)

    def get(self) -> numpy.array:
        return self.__image

    def set(self, image: numpy.array):
        self.__image = image
        self.height, self.width, *_ = self.__image.shape

    def copy(self) -> "Image":
        return Image(self.__image, self.image_name)

    def _apply_action(self, action: type, action_number: str = None):
        menu = self._get_menu(action)
        if action_number is None:
            self._print_menu(menu)
            action_number = input('> ')
        image_contrast = menu[action_number]()
        image = Image(self.__image, self.image_name + '*' if not self.image_name.endswith('*') else self.image_name)
        image_contrast.apply(image)
        return image

    def _get_threshold(self, threshold: int) -> int:
        pixels = self.get()
        brightness_map = [0 for _ in range(256)]
        pixels_count = self.width * self.height
        for i in range(self.height):
            for j in range(self.width):
                brightness_map[get_pixel_brightness(pixels[i, j])] += 1
        brightness_map = list(map(lambda x: x / pixels_count, brightness_map))
        threshold_percent = 0
        for i, brightness_rate in enumerate(brightness_map):
            if threshold_percent >= (threshold / 100):
                return i
            threshold_percent += brightness_rate

    @staticmethod
    def _get_menu(menu_class: type) -> dict[str]:
        return {
            str(i): cls for i, cls in enumerate(menu_class.__subclasses__())
        }

    @staticmethod
    def _print_menu(menu: dict[str]) -> None:
        print(f'Выберите тип преобразования:')
        for key, command in sorted(menu.items(), key=lambda item: item[0] if item[0] != '0' else '@'):
            print(f'{key: <3} - {command.__doc__}')
