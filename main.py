import pygame
import requests

pygame.font.init()

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.value = 0


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((450, 450))
        pygame.display.set_caption("Sudoku Solver")

        self.clock = pygame.time.Clock()
        self.running = True

    def start_game(self):
        self.grid = [[Cell(x, y) for x in range(9)] for y in range(9)]
        board = requests.get("https://sugoku.herokuapp.com/board?difficulty=random").json()['board']
        for y in range(9):
            for x in range(9):
                self.grid[y][x].value = board[y][x]

    def draw_grid(self):
        for y in range(1, 9):
            if y%3 == 0:
                pygame.draw.line(self.screen, (0, 0, 0), (0, y*50), (450, y*50), 3)
            else:
                pygame.draw.line(self.screen, (0, 0, 0), (0, y*50), (450, y*50))
        for x in range(1, 9):
            if x%3 == 0:
                pygame.draw.line(self.screen, (0, 0, 0), (x*50, 0), (x*50, 450), 3)
            else:
                pygame.draw.line(self.screen, (0, 0, 0), (x*50, 0), (x*50, 450))

    def draw_numbers(self):
        font = pygame.font.SysFont("Consolas", 35)
        for row in self.grid:
            for cell in row:
                if cell.value != 0:
                    text = font.render(str(cell.value), True, (0, 0, 0))
                    rect = text.get_rect()
                    rect.center = (cell.x*50 + 25, cell.y*50 + 25)
                    self.screen.blit(text, rect)

    def run(self):
        self.start_game()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
            self.screen.fill((255, 255, 255))

            self.draw_grid()
            self.draw_numbers()

            self.clock.tick(60)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()