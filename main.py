import pygame
import requests
import json
import random

pygame.font.init()

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.value = 0
        self.block = False


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((450, 450))
        pygame.display.set_caption("Sudoku Solver")

        self.clock = pygame.time.Clock()
        self.running = True
        self.current_scene = "home"

        self.current = None
        self.key_map = []
        for i, x in enumerate(range(49, 58)):
            self.key_map.append([x, i+1])
        self.home_bg = pygame.image.load("home.png")

    def start_game(self):
        self.grid = [[Cell(x, y) for x in range(9)] for y in range(9)]
        try:
            board = requests.get("https://sugoku.herokuapp.com/board?difficulty=random").json()['board']
            self.solution = requests.post("https://sugoku.herokuapp.com/solve", data={"board": str(board)}, headers={'Content-Type': 'application/x-www-form-urlencoded'}).json()['solution']
        except:
            board, self.solution = random.choice(json.load(open("offline.json", "r")))
        for y in range(9):
            for x in range(9):
                val = board[y][x]
                if val != 0:
                    self.grid[y][x].block = True
                self.grid[y][x].value = val

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
    
    def check(self):
        for row in self.grid:
            for cell in row:
                x, y = cell.x, cell.y
                if cell.value != self.solution[y][x]:
                    pygame.draw.rect(self.screen, (255, 0, 0), (x*50, y*50, 50, 50))

    def play(self):
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            x = pos[0]-pos[0]%50
            y = pos[1]-pos[1]%50
            if not self.grid[y//50][x//50].block:
                self.current = [x, y]
        keys = pygame.key.get_pressed()
        if self.current:
            x, y = self.current
            pygame.draw.rect(self.screen, (255, 0, 0), (x, y, 50, 50), 3)
            for key, value in self.key_map:
                if keys[int(key)]:
                    self.grid[y//50][x//50].value = value
        if keys[pygame.K_SPACE]:
            self.check()
        self.draw_grid()
        self.draw_numbers()

    def possible(self, cell, value):
        x, y = cell.x, cell.y
        for index, row in enumerate(self.grid):
            if self.grid[y][index].value == value:
                return False
            if self.grid[index][x].value == value:
                return False
        x0 = x//3*3
        y0 = y//3*3
        for i in range(3):
            for j in range(3):
                if self.grid[y0+i][x0+j].value == value:
                    return False
        return True
    
    def home(self):
        self.screen.blit(self.home_bg, (0, 0))
        play_btn_rect = pygame.Rect(130, 260, 190, 60)
        auto_rect = pygame.Rect(130, 330, 190, 60)
        if pygame.mouse.get_pressed()[0]:
            if play_btn_rect.collidepoint(pygame.mouse.get_pos()):
                self.current_scene = "play"
            if auto_rect.collidepoint(pygame.mouse.get_pos()):
                self.current_scene = "auto"

    def run(self):
        self.start_game()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
            self.screen.fill((255, 255, 255))

            if self.current_scene == "home":
                self.home()
            elif self.current_scene == "play":
                self.play()

            self.clock.tick(60)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()