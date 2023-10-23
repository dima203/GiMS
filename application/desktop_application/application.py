from application import Application


class DesktopApp(Application):
    def __init__(self) -> None:
        from .kivyapp import MainApp
        self.__app = MainApp()

    def run(self):
        self.__app.run()
