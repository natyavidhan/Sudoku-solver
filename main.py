import pygame

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((450, 450))
        pygame.display.set_caption("Sudoku Solver")

        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
            self.screen.fill((255, 255, 255))

            self.clock.tick(60)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()