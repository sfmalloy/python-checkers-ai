# from checkers_model import game
import board_model
from checkers_model import game_model

import pygame
import pygame.gfxdraw
from pygame.locals import *

class game_object(Rect):
    def __init__(self, x, y, w, h, tile_x, tile_y, color, state=None, hollow=False):
        super().__init__(x, y, w, h)
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.color = color
        self.state = state
        self.line_width = 0
        if hollow:
            self.line_width = 3

class gui_game:
    def __init__(self, screen, board):
        self.model = board
        self.tiles = []
        self.pieces = []
        self.highlighted = []
        self.length = len(self.model.grid)

        self.screen = screen

        self.square_length, _ = pygame.display.get_window_size()
        self.square_length //= self.length

        bright_color = True
        scale = .75
        self.piece_scale = self.square_length * scale

        for row in range(self.length):
            for col in range(self.length):
                self.tiles.append(game_object(self.square_length * col,
                                   self.square_length * row,
                                   self.square_length,
                                   self.square_length,
                                   col,
                                   row,
                                   (212, 186, 155) if bright_color else (128, 90, 45)))
                
                state = self.model.grid[row][col].state
                if state != board_model.tile_state.EMPTY:
                    self.pieces.append(game_object(self.tiles[-1].center[0] - self.piece_scale / 2, 
                                                 self.tiles[-1].center[1] - self.piece_scale / 2, 
                                                 self.piece_scale, 
                                                 self.piece_scale,
                                                 col,
                                                 row,
                                                 (255, 0, 0) if state == board_model.tile_state.PLAYER_1 else (0, 0, 0),
                                                 state=state))
                bright_color = not bright_color
            bright_color = not bright_color
    
    def draw_board(self):
        for t in self.tiles:
            pygame.draw.rect(self.screen, t.color, t)
        for p in self.pieces:
            pygame.gfxdraw.aacircle(self.screen, p.center[0], p.center[1], p.width // 2, p.color)
            pygame.gfxdraw.filled_circle(self.screen, p.center[0], p.center[1], p.width // 2, p.color)
        for h in self.highlighted:
            # Draw outer circle
            pygame.gfxdraw.aacircle(self.screen, h.center[0], h.center[1], h.width // 2, h.color)
            pygame.gfxdraw.filled_circle(self.screen, h.center[0], h.center[1], h.width // 2, h.color)

            # Draw inner circle
            pygame.gfxdraw.aacircle(self.screen, h.center[0], h.center[1], h.width // 3, (128, 90, 45))
            pygame.gfxdraw.filled_circle(self.screen, h.center[0], h.center[1], h.width // 3, (128, 90, 45))

    def highlight_moves(self, piece, dx, dy, tx, ty):
        if piece.state == board_model.tile_state.PLAYER_1:
            self.highlighted.append(game_object(piece.x + dx * self.square_length, 
                                                piece.y + dy * self.square_length,
                                                piece.width,
                                                piece.height,
                                                tx, 
                                                ty, 
                                                (255, 255, 255)))
        elif piece.state == board_model.tile_state.PLAYER_2:
            print(2)

if __name__ == '__main__':
    # Initializes all the modules
    pygame.init()
    WIN_LENGTH = 720
    screen = pygame.display.set_mode(size=(WIN_LENGTH, WIN_LENGTH))
    pygame.display.set_caption('Checkers')
    gm = game_model()
    g = gui_game(screen, gm.board())

    # Game loop
    running = True
    last_clicked = None
    while running:
        g.draw_board()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                found = False
                curr_paths = {}
                for p in g.pieces:
                    if p.collidepoint(event.pos):
                        g.highlighted.clear()
                        paths = g.model.get_moves(board_model.point(p.tile_x, p.tile_y), p.state)
                        for path in paths:
                            g.highlight_moves(p, path[-1].x - p.tile_x, path[-1].y - p.tile_y, path[-1].x, path[-1].y)
                        # g.highlight_moves(p)
                        last_clicked = p
                        found = True
                        break
                if not found:
                    for h in g.highlighted:
                        if h.collidepoint(event.pos):
                            # g.model.make_move(board_model.point(last_clicked.tile_x, last_clicked.tile_y), 
                            #                   board_model.point(h.tile_x, h.tile_y), 
                            #                   last_clicked.state)
                            last_clicked.x = h.x
                            last_clicked.y = h.y
                            last_clicked.width = h.width
                            last_clicked.height = h.height
                            last_clicked.tile_x = h.tile_x
                            last_clicked.tile_y = h.tile_y
                            found = True
                            break
                    if found:
                        g.highlighted.clear()

        pygame.display.flip()

    # Clean up and quit
    pygame.quit()
