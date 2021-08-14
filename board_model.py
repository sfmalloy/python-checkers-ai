from enum import Enum

class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

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

        x_diff = src.x - dest.x
        y_diff = src.y - dest.y

        if not self.grid[src.y][src.x].is_king:
            if player == tile_state.PLAYER_1 and y_diff < 0:
                return move_status.FAILED
            elif y_diff > 0: # is player 2, must be negative
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

    def make_move(self, src: point, dest: point, player: tile_state) -> move_status:
        status = self.is_legal_move(src, dest, player)
        if status == move_status.MOVED:
            if src.self.grid[src.y][src.x].is_king:
                self.grid[src.y][src.x].is_king = False
                self.grid[dest.y][dest.x].is_king = True
            self.grid[src.y][src.x].state = tile_state.EMPTY
            self.grid[dest.y][dest.x] = player

            # test for king transform
            if (player == tile_state.PLAYER_1 and dest.y == 7):
                self.grid[dest.y][dest.x].is_king = True
            elif (player == tile_state.PLAYER_2 and dest.y == 0):
                self.grid[dest.y][dest.x].is_king = True
        elif status == move_status.CAPTURED:
            y_offset = (src.x - dest.x) // 2
            x_offset = (src.y - dest.y) // 2
            self.grid[y_offset][x_offset].state = tile_state.EMPTY
            self.grid[y_offset][x_offset].is_king = tile_state.EMPTY

            if src.self.grid[src.y][src.x].is_king:
                self.grid[src.y][src.x].is_king = False
                self.grid[dest.y][dest.x].is_king = True
            self.grid[src.y][src.x].state = tile_state.EMPTY
            self.grid[dest.y][dest.x].state = player

            # test for king transform
            if (player == tile_state.PLAYER_1 and dest.y == 7):
                self.grid[dest.y][dest.x].is_king = True
            if (player == tile_state.PLAYER_2 and dest.y == 0):
                self.grid[dest.y][dest.x].is_king = True
        return status

    def is_legal_capture_move(self, src: point, dest: point, player: tile_state):
        # checking inputs
        if (player == tile_state.EMPTY): return move_status.FAILED
        if src.x < 0 or 7 < src.x: return move_status.FAILED
        if src.y < 0 or 7 < src.y: return move_status.FAILED
        if dest.x < 0 or 7 < dest.x: return move_status.FAILED
        if dest.y < 0 or 7 < dest.y: return move_status.FAILED
        if self.grid[src.y][src.x].state != player: return move_status.FAILED
        if self.grid[dest.y][dest.x].state != tile_state.EMPTY: return move_status.FAILED

        x_diff = src.x - dest.x
        y_diff = src.y - dest.y

        if not self.grid[src.y][src.x].is_king:
            if player == tile_state.PLAYER_1 and y_diff < 0:
                return move_status.FAILED
            elif y_diff > 0: # is player 2, must be negative
                return move_status.FAILED

        # is a two-space diagonal move that captures
        if abs(x_diff) == 2 and abs(y_diff) == 2:
            y_offset = y_diff // 2
            x_offset = x_diff // 2
            if (self.grid[y_offset][x_offset].state != tile_state.EMPTY and 
            self.grid[y_offset][x_offset].state != player):
                return move_status.CAPTURED
        # in all other cases the move is illegal
        return move_status.FAILED

    def make_capture_move(self, src: point, dest: point, player: tile_state):
        status = self.is_legal_move(src, dest, player)
        if status == move_status.MOVED:
            if src.self.grid[src.y][src.x].is_king:
                self.grid[src.y][src.x].is_king = False
                self.grid[dest.y][dest.x].is_king = True
            self.grid[src.y][src.x].state = tile_state.EMPTY
            self.grid[dest.y][dest.x] = player

            # test for king transform
            if (player == tile_state.PLAYER_1 and dest.y == 7):
                self.grid[dest.y][dest.x].is_king = True
            elif (player == tile_state.PLAYER_2 and dest.y == 0):
                self.grid[dest.y][dest.x].is_king = True
        elif status == move_status.CAPTURED:
            y_offset = (src.x - dest.x) // 2
            x_offset = (src.y - dest.y) // 2
            self.grid[y_offset][x_offset].state = tile_state.EMPTY
            self.grid[y_offset][x_offset].is_king = tile_state.EMPTY

            if src.self.grid[src.y][src.x].is_king:
                self.grid[src.y][src.x].is_king = False
                self.grid[dest.y][dest.x].is_king = True
            self.grid[src.y][src.x].state = tile_state.EMPTY
            self.grid[dest.y][dest.x].state = player

            # test for king transform
            if (player == tile_state.PLAYER_1 and dest.y == 7):
                self.grid[dest.y][dest.x].is_king = True
            if (player == tile_state.PLAYER_2 and dest.y == 0):
                self.grid[dest.y][dest.x].is_king = True
        return status
    
    # First move may be any move
    # If first move captured a piece
    #   make subsequent move
    def make_moves():
        return


if __name__ == '__main__':
    b = board()
    b.print()