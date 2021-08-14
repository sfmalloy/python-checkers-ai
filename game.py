# pygame GUI stuff
import pygame
from pygame.locals import *

class drawn_piece:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class game:
    def __init__(self, bot=None):
        self.width = self.height = 8
    
    def draw_board(self, screen):
        square_width, square_height = pygame.display.get_window_size()
        square_width //= self.width
        square_height //= self.height

        bright_color = True
        for row in range(self.height):
            for col in range(self.width):
                color = (212, 186, 155) if bright_color else (128, 90, 45)
                bright_color = not bright_color
                rect = Rect(square_width * col,
                            square_height * row,
                            square_width,
                            square_height)
                pygame.draw.rect(screen, color, rect)
            bright_color = not bright_color

# Initializes all the modules
pygame.init()

screen = pygame.display.set_mode(size=(720, 720))
g = game()

running = True
while running:
    g.draw_board(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    

# Clean up and quit
pygame.quit()
