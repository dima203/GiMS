import pickle

from .figure import Cube, Point

from OpenGL.GL import *
from OpenGL.GLUT import *


class Application:
    data_directory = r'./data/'
    __x_angle: float
    __y_angle: float
    __z_angle: float
    __shade_mode: int = GL_SMOOTH
    __polygon_mode: int = GL_FILL

    def __init__(self):
        self.__x_angle = 0
        self.__y_angle = 0
        self.__z_angle = 0

        v = (
            Point(-0.5, 0.5, -0.5, (1, 0, 0)),
            Point(0.5, 0.5, -0.5, (0, 1, 0)),
            Point(0.5, -0.5, -0.5, (0, 0, 1)),
            Point(-0.5, -0.5, -0.5, (1, 1, 0)),
            Point(-0.5, 0.5, 0.5, (0, 0, 1)),
            Point(0.5, 0.5, 0.5, (1, 1, 0)),
            Point(0.5, -0.5, 0.5, (1, 0, 0)),
            Point(-0.5, -0.5, 0.5, (0, 1, 0))
        )
        self.figure = Cube(v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7])

    def run(self) -> None:
        glutInit()

        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
        glutCreateWindow("CubeTest")
        glutReshapeWindow(800, 800)

        glutReshapeFunc(self.reshape)
        glutDisplayFunc(self.draw)
        glutKeyboardFunc(self.keyboard)
        glutTimerFunc(1000 // 60, self.timer, 60)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_POINT_SMOOTH)

        glPolygonMode(GL_FRONT_AND_BACK, self.__polygon_mode)
        glShadeModel(self.__shade_mode)

        glutMainLoop()

    def exit(self) -> None:
        exit(0)

    def reshape(self, width: int, height: int) -> None:
        glViewport(0, 0, width, height)

    def draw(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()
        glRotatef(self.__x_angle, 1, 0, 0)
        glRotatef(self.__y_angle, 0, 1, 0)
        glRotatef(self.__z_angle, 0, 0, 1)

        self.figure.draw()
        glutSwapBuffers()

    def timer(self, fps) -> None:
        glutTimerFunc(1000 // fps, self.timer, fps)
        glutPostRedisplay()

    def keyboard(self, key, x, y) -> None:
        if key == b'1':
            self.__polygon_mode = GL_LINE
            self.__shade_mode = GL_SMOOTH
        elif key == b'2':
            self.__polygon_mode = GL_POINT
            self.__shade_mode = GL_SMOOTH
        elif key == b'3':
            self.figure.fill_random()
            self.__polygon_mode = GL_FILL
            self.__shade_mode = GL_FLAT
        elif key == b'4':
            self.figure.fill_random()
            self.__polygon_mode = GL_FILL
            self.__shade_mode = GL_SMOOTH
        if key == b'5':
            self.__save_figure(input('Enter file name: '))
        if key == b'6':
            self.__load_figure(input('Enter file name: '))
        if key == b'w':
            self.__x_angle += 1
        elif key == b's':
            self.__x_angle -= 1
        if key == b'a':
            self.__y_angle -= 1
        elif key == b'd':
            self.__y_angle += 1
        if key == b'q':
            self.__z_angle += 1
        elif key == b'e':
            self.__z_angle -= 1
        if key == b'c':
            self.__x_angle = 0
            self.__y_angle = 0
            self.__z_angle = 0

        glPolygonMode(GL_FRONT_AND_BACK, self.__polygon_mode)
        glShadeModel(self.__shade_mode)

    def __save_figure(self, file_name: str) -> None:
        with open(self.data_directory + file_name, 'wb') as file:
            pickle.dump(self.figure.save(), file)

    def __load_figure(self, file_name: str) -> None:
        with open(self.data_directory + file_name, 'rb') as file:
            self.figure = self.figure.load(pickle.load(file))
