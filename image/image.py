import cv2

from random import randint

from filter import MedianCrossFilter
from contrast import CannyContrast
from effect import Effect
from .utils import get_pixel_brightness


class Image:
    base_images_dir = './images/'
    base_save_dir = './results/'

    def __init__(self, image=None, image_name: str = '') -> None:
        if image is None:
            self.__image = None
        else:
            self.__image = image.copy()
        self.image_name = image_name

    def get_image_name(self) -> str:
        return self.image_name

    @staticmethod
    def open() -> "Image":
        """Открыть изображение"""
        file_name = input('Введите имя файла: ')
        if not file_name.startswith(('/', './', '~/')):
            file_name = Image.base_images_dir + file_name
        return Image(cv2.imread(file_name), file_name)

    def save(self) -> "Image":
        """Сохранить изображение"""
        if self.__image is None:
            print('Изображение не открыто')
            return self
        file_name = input('Введите имя файла: ')
        if not file_name.startswith(('/', './', '~/')):
            file_name = Image.base_save_dir + file_name
        cv2.imwrite(file_name, self.__image)
        self.image_name = self.image_name if not self.image_name.endswith('*') else self.image_name[:-1]
        return self

    def show(self) -> "Image":
        """Просмотреть изображение"""
        if self.__image is None:
            print('Изображение не открыто')
            return self
        cv2.imshow('image', self.__image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return self

    def add_noise(self) -> "Image":
        """Добавить шум на изображение"""
        if self.__image is None:
            print('Изображение не открыто')
            return self
        probability = int(input('Введите вероятность шума: '))
        image = Image(self.__image, self.image_name+'*' if not self.image_name.endswith('*') else self.image_name)
        pixels = image.get()
        size = pixels.shape[0] * pixels.shape[1]
        count = (size * probability) // 100
        for i in range(count):
            x = randint(0, pixels.shape[0] - 1)
            y = randint(0, pixels.shape[1] - 1)
            pixels[x, y] = (randint(0, 255), randint(0, 255), randint(0, 255))
        return image

    def filter(self) -> "Image":
        """Отфильтровать изображение"""
        if self.__image is None:
            print('Изображение не открыто')
            return self
        image_filter = MedianCrossFilter(7)
        image = Image(self.__image, self.image_name+'*' if not self.image_name.endswith('*') else self.image_name)
        image_filter.filter(image)
        return image

    def contrast(self) -> "Image":
        """Получить контрастное изображение"""
        if self.__image is None:
            print('Изображение не открыто')
            return self
        image_contrast = CannyContrast(100, 200)
        image = Image(self.__image, self.image_name + '*' if not self.image_name.endswith('*') else self.image_name)
        image_contrast.contrast(image)
        return image

    def get_edge(self) -> "Image":
        """Получить контур изображения"""
        if self.__image is None:
            print('Изображение не открыто')
            return self
        image = Image(self.__image, self.image_name + '*' if not self.image_name.endswith('*') else self.image_name)
        pixels = image.get()
        threshold = int(input('Введите порог отсечения по гистограмме: '))
        e = image._get_threshold(threshold)
        for i in range(pixels.shape[0]):
            for j in range(pixels.shape[1]):
                pixels[i, j] = 0 if get_pixel_brightness(pixels[i, j]) > e else 2555
        return image


    def apply_effect(self) -> "Image":
        """Применить эффект"""
        if self.__image is None:
            print('Изображение не открыто')
            return self
        menu = self._get_menu(Effect)
        self._print_menu(menu)
        user_input = input('> ')
        image = Image(self.__image, self.image_name + '*' if not self.image_name.endswith('*') else self.image_name)
        effect = menu[user_input](image)
        effect.apply()
        return image

    def get(self):
        return self.__image

    def set(self, image):
        self.__image = image

    def copy(self) -> "Image":
        return Image(self.__image, self.image_name)

    def _get_threshold(self, threshold) -> int:
        pixels = self.get()
        brightness_map = [0 for _ in range(256)]
        pixels_count = pixels.shape[0] * pixels.shape[1]
        for i in range(pixels.shape[0]):
            for j in range(pixels.shape[1]):
                brightness_map[get_pixel_brightness(pixels[i, j])] += 1
        brightness_map = list(map(lambda x: x / pixels_count, brightness_map))
        threshold_percent = 0
        for i, brightness_rate in enumerate(brightness_map):
            if threshold_percent >= (threshold / 100):
                return i
            threshold_percent += brightness_rate

    def _get_menu(self, menu_class: type) -> dict[str]:
        return {
            str(i): cls for i, cls in enumerate(menu_class.__subclasses__())
        }

    def _print_menu(self, menu: dict[str]) -> None:
        print(f'Выберите тип преобразования:')
        for key, command in menu.items():
            print(f'{key: <3} - {command.__doc__}')
