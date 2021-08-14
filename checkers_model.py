from enum import Enum

from board_model import *

class game:
    def __init__ (self):
        self.board = board()
        self.turn = tile_state.PLAYER_1

    def make_turn(self, src: point, dest: point):
        status = self.board.make_move(src, dest, self.turn)
        if status == move_status.MOVED:
            if self.turn == tile_state.PLAYER_1:
                self.turn = tile_state.PLAYER_2
            else:
                self.turn = tile_state.PLAYER_2
