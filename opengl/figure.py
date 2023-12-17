from abc import ABC, abstractmethod
from typing import TypeAlias
import pickle
from random import choice
from copy import copy

from OpenGL.GL import *


Color: TypeAlias = tuple[float, float, float]

COLORS: list[Color] = [
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 1, 0),
    (1, 0, 1),
    (0, 1, 1)
]


class Figure(ABC):
    @abstractmethod
    def draw(self) -> None: ...

    @abstractmethod
    def fill_random(self) -> None: ...

    @abstractmethod
    def save(self) -> list[tuple] | tuple[float, float, float, Color]: ...

    @staticmethod
    @abstractmethod
    def load(data: list[tuple]) -> "Figure": ...


class Point(Figure):
    __x: float
    __y: float
    __z: float
    __color: Color

    def __init__(self, x: float, y: float, z: float, color: Color) -> None:
        self.__x = x
        self.__y = y
        self.__z = z
        self.__color = color

    def draw(self) -> None:
        glColor3fv(self.__color)
        glVertex3f(self.__x, self.__y, self.__z)

    def fill_random(self) -> None:
        self.__color = choice(COLORS)

    def save(self) -> tuple[float, float, float, Color]:
        return self.__x, self.__y, self.__z, self.__color

    @staticmethod
    def load(data: "Point") -> "Point":
        return data

    def __copy__(self) -> "Point":
        return Point(self.__x, self.__y, self.__z, self.__color)


class Face(Figure):
    __points: list[Point]

    def __init__(self, a: Point, b: Point, c: Point, d: Point) -> None:
        self.__points = [a, b, c, d]

    def draw(self) -> None:
        glPointSize(10.0)
        glLineWidth(5.0)
        glBegin(GL_QUAD_STRIP)
        for point in self.__points:
            point.draw()
        glEnd()
        glFlush()

    def fill_random(self) -> None:
        for point in self.__points:
            point.fill_random()

    def save(self) -> list[tuple]:
        results = []
        for point in self.__points:
            results.append(point.save())
        return results

    @staticmethod
    def load(data: list[tuple]) -> "Figure":
        points = []
        for point in data:
            points.append(Point.load(point))
        return Face(*points)


class Cube(Figure):
    __faces: list[Face]

    def __init__(self, v1: Point, v2: Point, v3: Point, v4: Point, v5: Point, v6: Point, v7: Point, v8: Point) -> None:
        self.__faces = []
        self.__faces.append(Face(copy(v1), copy(v2), copy(v4), copy(v3)))
        # self.__faces.append(Face(copy(v5), copy(v1), copy(v8), copy(v4)))
        # self.__faces.append(Face(copy(v6), copy(v5), copy(v7), copy(v8)))
        # self.__faces.append(Face(copy(v2), copy(v6), copy(v3), copy(v7)))
        # self.__faces.append(Face(copy(v5), copy(v6), copy(v1), copy(v2)))
        # self.__faces.append(Face(copy(v4), copy(v3), copy(v8), copy(v7)))

    def draw(self) -> None:
        for face in self.__faces:
            face.draw()

    def fill_random(self) -> None:
        for face in self.__faces:
            face.fill_random()

    def save(self) -> list[list]:
        results = []
        for face in self.__faces:
            results.append(face.save())
        return results

    @staticmethod
    def load(data: list[list]) -> "Cube":
        ...
