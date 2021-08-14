from enum import Enum

from board_model import *

class game_model:
    def __init__ (self):
        self.board = board()
        self.turn = tile_state.PLAYER_1

    def make_turn(self, src: point, moves: List[point]):
        status = self.board.make_turn(src, moves, self.turn)
        if status != move_status.FAILED:
            if self.turn == tile_state.PLAYER_1:
                self.turn = tile_state.PLAYER_2
            else:
                self.turn = tile_state.PLAYER_2
