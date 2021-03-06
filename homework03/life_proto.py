import pygame
import random
import copy

from pygame.locals import *
from typing import List, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(self, width: int=640, height: int=480, cell_size: int=10, speed: int=10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        self.grid = self.create_grid(randomize = True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.draw_lines()
            # Отрисовка списка клеток
            self.draw_grid()
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.grid = copy.deepcopy(self.get_next_generation())

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        if randomize:
            return [[random.randint(0, 1) for _ in range(self.cell_width)]
            for _ in range(self.cell_height)]
        else:
            return [[0] * self.cell_width for _ in range(self.cell_height)]

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        a = self.cell_size
        y = - a

        for i in range(len(self.grid)):
            x = 0
            y += a
            for j in range(len(self.grid[i])):
                if self.grid[i][j]:
                    pygame.draw.rect(self.screen, pygame.Color('green'),
                                    (x + 1, y + 1, a - 1, a - 1))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'),
                                    (x + 1, y + 1, a - 1, a - 1))
                x += a

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        i, j = cell

        neighbours = [self.grid[x][y] for x in range(i - 1, i + 2)
                for y in range(j - 1, j + 2) if (x, y) != cell and x >= 0
                and y >= 0 and x < len(self.grid) and y < len(self.grid[0])]

        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        nextg = copy.deepcopy(self.grid)
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                alive = sum(self.get_neighbours((i, j)))
                if self.grid[i][j]:
                    if alive != 2 and alive != 3:
                        nextg[i][j] = 0
                else:
                    if alive == 3:
                        nextg[i][j] = 1
        return nextg

if __name__ == '__main__':
    game = GameOfLife()
    game.run()
