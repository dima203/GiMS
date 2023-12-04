from random import randint, choice

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


SNAKES_COLORS = (
    ((0, 255, 0), (100, 255, 100)),
    ((0, 0, 255), (100, 100, 255)),
    ((255, 255, 0), (255, 255, 100)),
    ((255, 0, 255), (255, 100, 255)),
    ((0, 255, 255), (100, 255, 255)),
)


class Rectangle:
    window_x: int
    window_y: int
    size: int
    color: tuple[float, float, float]

    def __init__(self, x: int, y: int, size: int, color: tuple[int, int, int]) -> None:
        self.window_x = x
        self.window_y = y
        self.size = size
        self.color = color[0] / 255, color[1] / 255, color[2] / 255

    def move(self, new_x: int, new_y: int) -> None:
        self.window_x = new_x
        self.window_y = new_y

    def draw(self, window: pygame.Surface) -> None:
        window_center_x, window_center_y = window.get_width() // 2, window.get_height() // 2
        glColor3f(*self.color)
        glBegin(GL_QUADS)
        p1 = (self.window_x - window_center_x) / window_center_x
        p2 = (self.window_y - window_center_y) / window_center_y
        p3 = (self.window_x + self.size - window_center_x) / window_center_x
        p4 = (self.window_y + self.size - window_center_y) / window_center_y
        glVertex2f(p1, p2)
        glVertex2f(p3, p2)
        glVertex2f(p3, p4)
        glVertex2f(p1, p4)
        glEnd()
        glFlush()


class Brain:
    queue: list[tuple[tuple[int, int], int, tuple[int, int], float]]
    checked: list[tuple[tuple[int, int], int, tuple[int, int]]]
    path: list[int]

    def __init__(self) -> None:
        self.queue = []
        self.checked = []
        self.path = []

    def calculate_path(self, current_x: int, current_y: int, snakes: list["Head"], window) -> None:
        self.queue.clear()
        self.checked.clear()
        self.path.clear()

        self.__add_points(current_x, current_y, snakes)
        self.checked.append(((current_x, current_y), 0, (0, 0)))
        if len(FOODS) == 0:
            self.path.append(self.queue.pop()[1])
            return
        while len(self.queue) > 0:
            path_finded = False
            i, (current_pos, step, prev_pos, distance) = min(enumerate(self.queue), key=lambda x: x[1][3])
            self.queue.pop(i)
            for food in FOODS:
                if food.x == current_pos[0] and food.y == current_pos[1]:
                    while current_pos != (current_x, current_y):
                        self.path.append(step)
                        for pos in self.checked:
                            if pos[0] == prev_pos:
                                current_pos, step, prev_pos = pos
                                break
                    path_finded = True
                    break
            if path_finded:
                break
            self.__add_points(*current_pos, snakes)
            self.checked.append((current_pos, step, prev_pos))
        else:
            self.path.append(choice(self.checked)[1])

    def __add_points(self, current_x: int, current_y: int, snakes: list["Head"]):
        if current_x - 1 >= 0:
            step = 0
            point = (current_x - 1, current_y)
            if point not in map(lambda x: x[0], self.checked) and point not in map(lambda x: x[0], self.queue):
                for snake in snakes:
                    if snake.check_overlap(*point):
                        break
                else:
                    distance = min(((point[0] - food.x) ** 2 + (point[1] - food.y) ** 2)**0.5 for food in FOODS)
                    self.queue.append((point, step, (current_x, current_y), distance))
        if current_y + 1 <= FIELD_HEIGHT - 1:
            step = 1
            point = (current_x, current_y + 1)
            if point not in map(lambda x: x[0], self.checked) and point not in map(lambda x: x[0], self.queue):
                for snake in snakes:
                    if snake.check_overlap(*point):
                        break
                else:
                    distance = min(((point[0] - food.x) ** 2 + (point[1] - food.y) ** 2) ** 0.5 for food in FOODS)
                    self.queue.append((point, step, (current_x, current_y), distance))
        if current_x + 1 <= FIELD_WIDTH - 1:

            step = 2
            point = (current_x + 1, current_y)
            if point not in map(lambda x: x[0], self.checked) and point not in map(lambda x: x[0], self.queue):
                for snake in snakes:
                    if snake.check_overlap(*point):
                        break
                else:
                    distance = min(((point[0] - food.x) ** 2 + (point[1] - food.y) ** 2) ** 0.5 for food in FOODS)
                    self.queue.append((point, step, (current_x, current_y), distance))
        if current_y - 1 >= 0:
            step = 3
            point = (current_x, current_y - 1)
            if point not in map(lambda x: x[0], self.checked) and point not in map(lambda x: x[0], self.queue):
                for snake in snakes:
                    if snake.check_overlap(*point):
                        break
                else:
                    distance = min(((point[0] - food.x) ** 2 + (point[1] - food.y) ** 2) ** 0.5 for food in FOODS)
                    self.queue.append((point, step, (current_x, current_y), distance))


class Tail:
    figure: Rectangle
    next_part: "Tail" = None
    x: int
    y: int
    color: tuple[int, int, int]
    tail_color: tuple[int, int, int]

    def __init__(self, x: int, y: int, color: tuple[int, int, int] = (255, 100, 100)) -> None:
        self.x = x
        self.y = y
        self.color = color
        self.tail_color = color
        self.figure = Rectangle(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, self.color)

    def move(self, next_x: int, next_y: int) -> None:
        if self.next_part is not None:
            self.next_part.move(self.x, self.y)

        self.x, self.y = next_x, next_y
        self.figure.move(self.x * CELL_SIZE, self.y * CELL_SIZE)

    def draw(self, window: pygame.Surface) -> None:
        self.figure.draw(window)

        if self.next_part is None:
            return

        self.next_part.draw(window)

    def growth(self) -> None:
        if self.next_part is None:
            self.next_part = Tail(self.x, self.y, self.tail_color)
        else:
            self.next_part.growth()

    def decrease(self) -> bool:
        if self.next_part is None:
            return True
        elif self.next_part.next_part is None:
            del self.next_part
            self.next_part = None
            return False
        else:
            self.next_part.decrease()
            return False

    def check_overlap(self, x: int, y: int) -> bool:
        if self.x == x and self.y == y:
            return True
        else:
            if self.next_part is None:
                return False
            else:
                return self.next_part.check_overlap(x, y)

    def __repr__(self) -> str:
        return '-> T ' + str(self.next_part)


class Head(Tail):
    length: int = 1
    tail_length: int = 0
    current_length: int = 1
    brain: Brain = None
    keys: dict[int, ...] = None
    current_key: int = 0
    current_move: int = 0

    def __init__(self, x: int, y: int, length: int = 1,
                 colors_palet: tuple[tuple[int, int, int], tuple[int, int, int]] = SNAKES_COLORS[0]) -> None:
        super().__init__(x, y, colors_palet[1])
        self.keys = {}
        self.color = colors_palet[0]
        self.length = length
        self.figure = Rectangle(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, self.color)

    def add_length(self, n: int) -> None:
        self.length += n

    def add_brain(self, brain: Brain) -> None:
        self.brain = brain
        self.keys[1] = self.move_front
        self.keys[0] = self.move_left
        self.keys[3] = self.move_back
        self.keys[2] = self.move_right

    def add_keys(self, front: int, left: int, back: int, right: int) -> None:
        self.keys[front] = self.move_front
        self.keys[left] = self.move_left
        self.keys[back] = self.move_back
        self.keys[right] = self.move_right

    def step(self) -> bool:
        if self.tail_length < self.length - 1:
            self.growth()
            self.tail_length += 1

        if self.brain is not None:
            self.brain.calculate_path(self.x, self.y, SNAKES, pygame.display.get_surface())
            self.current_key = self.brain.path.pop()

        self.keys[self.current_key]()

        self.current_move += 1
        if self.current_move >= ENERGY_DECREASE_RATE_IN_TICK:
            self.current_move = 0
            self.length -= 1
            self.tail_length -= 1
            return self.decrease()

    def check_input(self, event: pygame.event.Event) -> None:
        if self.brain is None:
            if event.type == pygame.KEYDOWN and event.key in self.keys:
                self.current_key = event.key

    def move_front(self) -> None:
        self.move(self.x, self.y + 1)

    def move_left(self) -> None:
        self.move(self.x - 1, self.y)

    def move_back(self) -> None:
        self.move(self.x, self.y - 1)

    def move_right(self) -> None:
        self.move(self.x + 1, self.y)

    def __repr__(self) -> str:
        return 'H ' + str(self.next_part)


class Food:
    figure: Rectangle
    x: int
    y: int
    color: tuple[int, int, int] = (255, 100, 100)
    energy: int = 1

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.figure = Rectangle(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, self.color)

    def draw(self, window: pygame.Surface) -> None:
        self.figure.draw(window)


class SuperFood(Food):
    color: tuple[int, int, int] = (255, 0, 0)
    energy: int = 5


WINDOW_SIZE = (1920, 1020)
FPS = 60
TICK_TIME = 300
CELL_SIZE = 30
FIELD_WIDTH, FIELD_HEIGHT = WINDOW_SIZE[0] // CELL_SIZE, WINDOW_SIZE[1] // CELL_SIZE

TIME = 0
FOOD_TIME = 0
MAX_FOOD = 30
FOOD_SPAWN_RATE_IN_TICK = 4
ENERGY_DECREASE_RATE_IN_TICK = 1000
FOODS: list[Food] = []
SNAKES: list[Head] = []


def spawn_food() -> None:
    global FOODS

    if len(FOODS) >= MAX_FOOD:
        return

    for _ in range(5):
        food_x, food_y = randint(0, FIELD_WIDTH - 1), randint(0, FIELD_HEIGHT - 1)
        for snake in SNAKES:
            if snake.check_overlap(food_x, food_y):
                continue

        if randint(0, 10) == 10:
            food = SuperFood(food_x, food_y)
        else:
            food = Food(food_x, food_y)
        FOODS.append(food)
        break


def game_end() -> None:
    pygame.quit()
    quit()


def main():
    global SCORE
    global TIME
    global FOOD_TIME
    global SNAKES

    pygame.init()
    window = pygame.display.set_mode(WINDOW_SIZE, DOUBLEBUF | OPENGL)

    clock = pygame.time.Clock()

    glClearColor(0, 0, 0, 1)

    snake1 = Head(0, 0, 5, SNAKES_COLORS[0])
    snake1.add_brain(Brain())
    # snake1.add_keys(pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT)
    # snake1.current_key = pygame.K_UP
    SNAKES.append(snake1)

    snake2 = Head(FIELD_WIDTH - 1, 0, 5, SNAKES_COLORS[1])
    snake2.add_brain(Brain())
    SNAKES.append(snake2)

    snake3 = Head(FIELD_WIDTH - 1, FIELD_HEIGHT - 1, 5, SNAKES_COLORS[2])
    snake3.add_brain(Brain())
    SNAKES.append(snake3)

    snake4 = Head(0, FIELD_HEIGHT - 1, 5, SNAKES_COLORS[3])
    snake4.add_brain(Brain())
    SNAKES.append(snake4)

    snake5 = Head(FIELD_WIDTH // 2, FIELD_HEIGHT // 2, 5, SNAKES_COLORS[4])
    snake5.add_brain(Brain())
    SNAKES.append(snake5)

    FOODS.append(Food(10, 10))
    FOODS.append(Food(FIELD_WIDTH - 10, 10))
    FOODS.append(Food(FIELD_WIDTH - 1, FIELD_HEIGHT - 10))
    FOODS.append(Food(10, FIELD_HEIGHT - 10))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
            for snake in SNAKES:
                snake.check_input(event)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if TIME >= TICK_TIME:
            TIME -= TICK_TIME
            for snake in SNAKES:
                if snake.step():
                    SNAKES.remove(snake)
        if FOOD_TIME >= FOOD_SPAWN_RATE_IN_TICK * TICK_TIME:
            FOOD_TIME -= FOOD_SPAWN_RATE_IN_TICK * TICK_TIME
            spawn_food()

        for snake in SNAKES:
            for food in FOODS:
                if snake.x == food.x and snake.y == food.y:
                    snake.add_length(food.energy)
                    FOODS.remove(food)
                    break

        for snake in SNAKES:
            for other_snake in SNAKES:
                if snake != other_snake:
                    if other_snake.check_overlap(snake.x, snake.y):
                        other_snake.add_length(snake.length)
                        SNAKES.remove(snake)
                        break
                else:
                    if other_snake.next_part is not None and other_snake.next_part.check_overlap(snake.x, snake.y):
                        other_snake.add_length(snake.length)
                        SNAKES.remove(snake)
                        break

        for snake in SNAKES:
            if not 0 <= snake.x <= FIELD_WIDTH - 1 or not 0 <= snake.y <= FIELD_HEIGHT - 1:
                SNAKES.remove(snake)

        if len(SNAKES) <= 1:
            game_end()

        for food in FOODS:
            food.draw(window)
        for snake in SNAKES:
            snake.draw(window)

        pygame.display.flip()
        clock.tick(FPS)

        TIME += clock.get_time()
        FOOD_TIME += clock.get_time()


if __name__ == '__main__':
    main()
