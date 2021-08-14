from enum import Enum
from typing import List

class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f'({self.x},{self.y})'

class tile_state(Enum):
    EMPTY    = 0
    PLAYER_1 = 1
    PLAYER_2 = 2

class move_status(Enum):
    FAILED   = 0
    MOVED    = 1
    CAPTURED = 2

class tile:
    def __init__ (self, state: tile_state):
        self.state: tile_state = state
        self.is_king: bool       = False

class board:
    def __init__(self):
        self.grid = []
        # init player 1
        for i in range(3):
            row = []
            for j in range(8):
                if i % 2 == 0:
                    if j % 2 == 0:
                        row.append(tile(tile_state.EMPTY))
                    else:
                        row.append(tile(tile_state.PLAYER_1))
                else:
                    if j % 2 == 0:
                        row.append(tile(tile_state.PLAYER_1))
                    else:
                        row.append(tile(tile_state.EMPTY))
            self.grid.append(row)
        # init no mans land
        for i in range(2):
            row = []
            for j in range(8):
                row.append(tile(tile_state.EMPTY))
            self.grid.append(row)
        # init player 2
        for i in range(3):
            row = []
            for j in range(8):
                if i % 2 == 0:
                    if j % 2 == 0:
                        row.append(tile(tile_state.PLAYER_2))
                    else:
                        row.append(tile(tile_state.EMPTY))
                else:
                    if j % 2 == 0:
                        row.append(tile(tile_state.EMPTY))
                    else:
                        row.append(tile(tile_state.PLAYER_2))
            self.grid.append(row)
                
    
    def print(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                print(self.grid[i][j].state.value, end=' ')
            print()

    
    def is_legal_move(self, src: point, dest: point, player: tile_state) -> move_status:
        # checking inputs
        if (player == tile_state.EMPTY): return move_status.FAILED
        if src.x < 0 or 7 < src.x: return move_status.FAILED
        if src.y < 0 or 7 < src.y: return move_status.FAILED
        if dest.x < 0 or 7 < dest.x: return move_status.FAILED
        if dest.y < 0 or 7 < dest.y: return move_status.FAILED
        if self.grid[src.y][src.x].state != player: return move_status.FAILED
        if self.grid[dest.y][dest.x].state != tile_state.EMPTY: return move_status.FAILED

        x_diff = dest.x - src.x
        y_diff = dest.y - src.y

        if not self.grid[src.y][src.x].is_king:
            if player == tile_state.PLAYER_1 and y_diff <= 0:
                return move_status.FAILED
            if player == tile_state.PLAYER_2 and y_diff >= 0:
                return move_status.FAILED
        
        # is a one-space diagonal move
        if abs(x_diff) == 1 and abs(y_diff) == 1:
            return move_status.MOVED
        # is a two-space diagonal move that captures
        if abs(x_diff) == 2 and abs(y_diff) == 2:
            y_offset = y_diff // 2
            x_offset = x_diff // 2
            if (self.grid[y_offset][x_offset].state != tile_state.EMPTY and 
            self.grid[y_offset][x_offset].state != player):
                return move_status.CAPTURED
        # in all other cases the move is illegal
        return move_status.FAILED

    def get_moves(self, src: point, player: tile_state, has_captured: bool = False, prev_moves: List[point] = []) -> List[List[point]]:
        legal_moves = []
        # checking 1-space moves - initial cases
        if not has_captured:
            up_right = point(src.x + 1, src.y - 1)
            if self.is_legal_move(src, up_right, player) != move_status.FAILED:
                legal_moves.append([up_right])
            up_left = point(src.x - 1, src.y - 1)
            if self.is_legal_move(src, up_left, player) != move_status.FAILED:
                legal_moves.append([up_left])
            down_right = point(src.x + 1, src.y + 1)
            if self.is_legal_move(src, down_right, player) != move_status.FAILED:
                legal_moves.append([down_right])
            down_left = point(src.x - 1, src.y + 1)
            if self.is_legal_move(src, down_left, player) != move_status.FAILED:
                legal_moves.append([down_left])

       # checking 2-space moves - recursive cases
        up_right = point(src.x + 2, src.y - 2)
        if self.is_legal_move(src, up_right, player) != move_status.FAILED:
            temp = prev_moves.append(up_right)
            legal_moves.append(self.get_moves(up_right, player, True, temp))

        up_left = point(src.x - 2, src.y - 2)
        if self.is_legal_move(src, up_left, player) != move_status.FAILED:
            temp = prev_moves.append(up_left)
            legal_moves.append(self.get_moves(up_left, player, True, temp))

        down_right = point(src.x + 2, src.y + 2)
        if self.is_legal_move(src, down_right, player) != move_status.FAILED:
            temp = prev_moves.append(down_right)
            legal_moves.append(self.get_moves(down_right, player, True, temp))

        down_left = point(src.x - 2, src.y + 2)
        if self.is_legal_move(src, down_left, player) != move_status.FAILED:
            temp = prev_moves.append(down_left)
            legal_moves.append(self.get_moves(down_left, player, True, temp))
        return list(filter(lambda x: x, legal_moves))

    def remove_piece(self, move: point):
        self.grid[move.y][move.x].state = tile_state.EMPTY
        self.grid[move.y][move.x].is_king = False

    def make_move(self, src: point, dest: point, player: tile_state):
        if not self.is_legal_move(src, dest, player): return move_status.FAILED
        
        x_diff = dest.x - src.x
        y_diff = dest.y - src.y

        if abs(x_diff) == 1 and abs(y_diff) == 1: # move one tile
            self.grid[dest.y][dest.x].state = player
            self.grid[dest.y][dest.x].is_king = self.grid[src.y][src.x].is_king
            self.remove_piece(src)
            return move_status.MOVED
        
        if abs(x_diff) == 2 and abs(y_diff) == 2: # move two tiles
            self.grid[dest.y][dest.x].state = player
            self.grid[dest.y][dest.x].is_king = self.grid[src.y][src.x].is_king
            self.remove_piece(src)
            self.remove_piece(point(y_diff // 2, x_diff // 2))
            return move_status.CAPTURED

        return move_status.FAILED

    def make_turn(self, src: point, moves: List[point], player: tile_state):
        for move in moves:
            status = make_move(src, move, player)
            if status == move_status.FAILED:
                return False
        return True
        


if __name__ == '__main__':
    b = board()
    b.print()
    print(b.get_moves(point(1,2), tile_state.PLAYER_1))

