import pathlib
import random
import copy

from typing import List, Optional, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(
        self,
        size: Tuple[int, int],
        randomize: bool=True,
        max_generations: Optional[float]=float('inf')
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=True)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool=False) -> Grid:
        if randomize:
            return [[random.randint(0, 1) for _ in range(self.rows)]
            for _ in range(self.cols)]
        else:
            return [[0] * self.rows for _ in range(self.cols)]

    def get_neighbours(self, cell: Cell) -> Cells:
        i, j = cell

        neighbours = [self.curr_generation[x][y] for x in range(i - 1, i + 2)
                for y in range(j - 1, j + 2) if (x, y) != cell and x >= 0
                and y >= 0 and x < len(self.curr_generation)
                and y < len(self.curr_generation[0])]

        return neighbours

    def get_next_generation(self) -> Grid:
        nextg = copy.deepcopy(self.curr_generation)
        for i in range(len(self.curr_generation)):
            for j in range(len(self.curr_generation[i])):
                alive = sum(self.get_neighbours((i, j)))
                if self.curr_generation[i][j]:
                    if alive != 2 and alive != 3:
                        nextg[i][j] = 0
                else:
                    if alive == 3:
                        nextg[i][j] = 1

        return nextg

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.max_generations == self.generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        num_lines = sum(1 for line in open(filename))
        value = [c for c in open(filename).read() if c in '10']
        values = list(map(int, value))
        v = [values[i:i+num_lines] for i in range(0, len(values), num_lines)]
        life = GameOfLife((len(v), len(v[0])))
        life.curr_generation = v

        return life

    def save(filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        result = open(filename, 'w')
        for i in range(len(self.curr_generation)):
            result.write(''.join(map(str, self.curr_generation[i])) + '\n')
        result.close()
