from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarListItem
from kivymd.uix.button import MDFlatButton
from kivymd.toast import toast

from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty

import cv2

import os

import imglib.image
from filter import Filter
from contrast import Contrast
from effect import Effect


class Item(OneLineAvatarListItem):
    divider = None
    menu_id = StringProperty()
    source = StringProperty()


class SelectValueDialog(MDBoxLayout):
    value = NumericProperty()


class WriteTextDialog(MDBoxLayout):
    value = StringProperty()


class MainApp(MDApp):
    kv_directory = './application/desktop_application/kivyapp/kv'

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.__image = imglib.image.Image()

        self.open_manager_open = False
        self.open_manager = MDFileManager(
            exit_manager=self.exit_open_manager, select_path=self.open_path
        )
        self.save_manager_open = False
        self.save_manager = MDFileManager(
            exit_manager=self.exit_save_manager, select_path=self.save_path, search='dirs'
        )

    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Teal'
        self.theme_cls.accent_palette = 'Red'
        self.theme_cls.accent_hue = '900'
        self.error_color = "#FF0000"
        self.save_color = '#00FF00'

        Clock.schedule_interval(self.update_image, 0.25)

    def update_image(self, dt) -> None:
        buf = cv2.flip(self.__image.get(), 0)
        buf = buf.tostring()
        texture = Texture.create(size=(self.__image.width, self.__image.height), colorfmt='bgr')
        texture.blit_buffer(buf, bufferfmt="ubyte", colorfmt="bgr")
        self.root.ids.image.texture = texture

    def open_image(self) -> None:
        self.open_manager.show(os.getcwd() + r'\images')
        self.open_manager_open = True

    def save_image(self) -> None:
        self.save_manager.show(os.getcwd() + r'\results')
        self.save_manager_open = True

    def open_path(self, path: str):
        self.exit_open_manager()
        self.__image = self.__image.open(path)

    def save_path(self, path: str):
        self.save_path = path
        self.dialog = MDDialog(
            title='Введите название файла',
            type='custom',
            content_cls=WriteTextDialog(),
            buttons=[
                MDFlatButton(text='Cancel', on_release=self.close_dialog),
                MDFlatButton(text='Apply', on_release=self.save_image_path)
            ]
        )
        self.dialog.open()

    def save_image_path(self, callback) -> None:
        self.dialog.dismiss()
        self.exit_save_manager()
        self.__image = self.__image.save(self.save_path + '\\' + self.dialog.content_cls.ids.field.text)
        toast('Сохранено')

    def exit_open_manager(self, *args):
        self.open_manager_open = False
        self.open_manager.close()

    def exit_save_manager(self, *args):
        self.save_manager_open = False
        self.save_manager.close()

    def noise_image(self) -> None:
        self.dialog = MDDialog(
            title='Выберите количество шума',
            type='custom',
            content_cls=SelectValueDialog(),
            buttons=[
                MDFlatButton(text='Отменить', on_release=self.close_dialog),
                MDFlatButton(text='Принять', on_release=self.add_noise)
            ]
        )
        self.dialog.open()

    def add_noise(self, callback) -> None:
        self.dialog.dismiss()
        self.__image = self.__image.add_noise(int(self.dialog.content_cls.ids.slider.value))
        toast('Выполнено')

    def filter_image(self) -> None:
        filter_menu = self.__image._get_menu(Filter)
        self.dialog = MDDialog(
            title='Выберите метод фильтрации',
            type='simple',
            items=[
                Item(text=item.__doc__, menu_id=key, on_release=self.filter_select)
                for key, item in sorted(filter_menu.items(), key=lambda item: item[0] if item[0] != '0' else '@')
            ]
        )
        self.dialog.open()

    def filter_select(self, callback) -> None:
        self.dialog.dismiss()
        self.__image = self.__image.filter(callback.menu_id)
        toast('Выполнено')

    def contrast_image(self) -> None:
        contrast_menu = self.__image._get_menu(Contrast)
        self.dialog = MDDialog(
            title='Выберите метод контрастирования',
            type='simple',
            items=[
                Item(text=item.__doc__, menu_id=key, on_release=self.contrast_select)
                for key, item in sorted(contrast_menu.items(), key=lambda item: item[0] if item[0] != '0' else '@')
            ]
        )
        self.dialog.open()

    def contrast_select(self, callback) -> None:
        self.dialog.dismiss()
        self.__image = self.__image.contrast(callback.menu_id)
        toast('Выполнено')

    def edge_image(self) -> None:
        self.dialog = MDDialog(
            title='Выберите порог отсечения',
            type='custom',
            content_cls=SelectValueDialog(),
            buttons=[
                MDFlatButton(text='Cancel', on_release=self.close_dialog),
                MDFlatButton(text='Apply', on_release=self.get_edge)
            ]
        )
        self.dialog.open()

    def get_edge(self, callback) -> None:
        self.dialog.dismiss()
        self.__image = self.__image.get_edge(int(self.dialog.content_cls.ids.slider.value))
        toast('Выполнено')

    def effect_image(self) -> None:
        contrast_menu = self.__image._get_menu(Effect)
        self.dialog = MDDialog(
            title='Выберите эффект',
            type='simple',
            items=[
                Item(text=item.__doc__, menu_id=key, on_release=self.effect_select)
                for key, item in sorted(contrast_menu.items(), key=lambda item: item[0] if item[0] != '0' else '@')
            ]
        )
        self.dialog.open()

    def effect_select(self, callback) -> None:
        self.dialog.dismiss()
        self.__image = self.__image.effect(callback.menu_id)
        toast('Выполнено')

    def close_dialog(self, callback) -> None:
        self.dialog.dismiss()
