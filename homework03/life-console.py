import curses
import os

from life import GameOfLife
from ui import UI


class Console(UI):

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.border('|', '|', '-', '-', '+', '+', '+', '+')

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for i in range(len(self.life.curr_generation)):
            for j in range(len(self.life.curr_generation[i])):
                if self.life.curr_generation[i][j]:
                    screen.addstr(j + 1, i + 1, '*')
                else:
                    screen.addstr(j + 1, i + 1, ' ')

    def run(self) -> None:
        screen = curses.initscr()

        running = True
        while self.life.is_changing:
            while not self.life.is_max_generations_exceeded:
                while running:
                    self.draw_borders(screen)
                    self.draw_grid(screen)
                    self.life.step()
                    screen.refresh()
        curses.endwin()
