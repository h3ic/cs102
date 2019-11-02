import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):

    def __init__(self, life: GameOfLife, cell_size: int=10, speed: int=10) -> None:
        super().__init__(life)

        self.cell_size = cell_size

        self.width = self.life.rows * self.cell_size
        self.height = self.life.cols * self.cell_size
        self.screen_size = self.width, self.height

        self.screen = pygame.display.set_mode(self.screen_size)

        self.cell_width = self.width // self.life.cols
        self.cell_height = self.height // self.life.rows

        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))

    def draw_grid(self) -> None:
        a = self.cell_size
        y = - a

        for i in range(len(self.life.curr_generation)):
            x = 0
            y += a
            for j in range(len(self.life.curr_generation[i])):
                if self.life.curr_generation[i][j]:
                    pygame.draw.rect(self.screen, pygame.Color('green'),
                                    (x + 1, y + 1, a - 1, a - 1))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'),
                                    (x + 1, y + 1, a - 1, a - 1))
                x += a

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        self.life.create_grid(True)
        self.paused = False

        running = True
        while running:
            while self.life.is_changing:
                while not self.life.is_max_generations_exceeded:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                self.paused = not self.paused
                        elif event.type == pygame.MOUSEBUTTONUP:
                            x, y = event.pos
                            x //= self.cell_size
                            y //= self.cell_size
                            self.life.curr_generation[y][x] = \
                                int(not bool(self.life.curr_generation[y][x]))
                            self.draw_grid()
                            pygame.display.flip()

                    if self.paused:
                        self.draw_grid()
                        pygame.display.flip()
                        continue

                    self.draw_lines()
                    self.draw_grid()
                    self.life.step()

                    pygame.display.flip()
                    clock.tick(self.speed)
        pygame.quit()

if __name__ == '__main__':
    ui = GUI(GameOfLife((64, 48), True))
    ui.run()