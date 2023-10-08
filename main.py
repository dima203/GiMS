from image.image import Image


class Application:
    def __init__(self) -> None:
        self.__image: Image | None = Image()
        self.__menu = self.__create_menu()

    def run(self) -> None:
        self.cycle()

    def cycle(self) -> None:
        try:
            while True:
                self._print_menu()
                user_input = self._get_user_input()
                self._handle_user_input(user_input)
        except KeyboardInterrupt:
            return

    def stop(self) -> None:
        """Завершение программы"""
        raise KeyboardInterrupt

    def _print_menu(self) -> None:
        print(f'Открыто изображение: {self.__image.get_image_name()}')
        for key, command in self.__menu.items():
            print(f'{key: <3} - {command.__doc__}')

    def _get_user_input(self) -> str:
        while True:
            user_input = input('> ')
            try:
                self.__menu[user_input]
            except KeyError:
                print('Такой команды нет')
                continue
            return user_input

    def _handle_user_input(self, user_input: str) -> None:
        self.__image = self.__menu[user_input]()
        self.__menu = self.__create_menu()

    def __create_menu(self) -> dict[str]:
        return {
            '1': self.__image.open,
            '2': self.__image.save,
            '3': self.__image.show,
            '4': self.__image.add_noise,
            '5': self.__image.filter,
            '6': self.__image.contrast,
            '7': self.__image.get_edge_image,
            '0': self.stop
        }


if __name__ == '__main__':
    app = Application()
    app.run()
