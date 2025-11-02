class game_state:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.move_functions = {'p': self.get_pawn_moves,
                               'R': self.get_rook_moves,
                               'N': self.get_knight_moves,
                               'B': self.get_bishop_moves,
                               'K': self.get_king_moves,
                               'Q': self.get_queen_moves}
        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.check_mate = False
        self.stale_mate = False

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
        if move.piece_moved == "wK":
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == "bK":
            self.black_king_location = (move.end_row, move.end_col)


    def undo_move(self):
        if len(self.move_log) > 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move
            if move.piece_moved == "wK":
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == "bK":
                self.black_king_location = (move.start_row, move.start_col)

    def get_valid_moves(self):

        moves = self.get_all_possible_moves()

        for i in range(len(moves) - 1, -1, -1):
            self.make_move(moves[i])
            self.white_to_move = not self.white_to_move
            if self.in_check():
                moves.remove(moves[i])
            self.undo_move()
            self.white_to_move = not self.white_to_move
            if len(moves) == 0:
                if self.in_check():
                    self.check_mate = True
                else:
                    self.stale_mate = True
            else:
                self.check_mate = False
                self.stale_mate = False
        return moves

    def in_check(self):
        if self.white_to_move:
            return self.square_under_attack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.square_under_attack(self.black_king_location[0], self.black_king_location[1])

    def square_under_attack(self, r, c):
        self.white_to_move = not self.white_to_move
        opp_moves = self.get_all_possible_moves()
        self.white_to_move = not self.white_to_move
        for mv in opp_moves:
            if mv.end_row == r and mv.end_col == c:
                return True
        return False


    def get_all_possible_moves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    # print("here")
                    piece = self.board[r][c][1]
                    self.move_functions[piece](r, c, moves)
                    print(*moves)
        return moves

    def get_pawn_moves(self, r, c, moves):
        if self.white_to_move:
            if self.board[r - 1][c] == "--":
                moves.append(move((r,c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":
                    moves.append(move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(move((r, c), (r - 1, c + 1), self.board))
        else:
            if self.board[r+1][c] == "--":
                moves.append(move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(move((r, c), (r + 1, c + 1), self.board))


    def get_rook_moves(self, r, c, moves):
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece =  self.board[end_row][end_col]
                    if end_piece== '--':
                        moves.append(move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(move((r, c), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break


    def get_knight_moves(self, r, c, moves):
        directions = [(2, 1), (-2, 1), (2, -1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            end_row = r + d[0]
            end_col = c + d[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece == "--" or end_piece[0] == enemy_color:
                    moves.append(move((r, c), (end_row, end_col), self.board))


    def get_bishop_moves(self, r, c, moves):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(move((r, c), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break
    def get_queen_moves(self, r, c, moves):
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(move((r, c), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def get_king_moves(self, r, c, moves):
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            end_row = r + d[0]
            end_col = c + d[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece == "--" or end_piece[0] == enemy_color:
                    moves.append(move((r, c), (end_row, end_col), self.board))


class move:
    ranks_to_rows = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}

    file_to_cols = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    cols_to_file = {v: k for k, v in file_to_cols.items()}

    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
        print(self.move_id)

    # def __eq__(self, other):
    #     if isinstance(other, move):
    #         return self.move_id == other.move_id
    #     return False
    def __eq__(self, other):
        if isinstance(other, move):
            return (self.start_row == other.start_row and
                    self.start_col == other.start_col and
                    self.end_row == other.end_row and
                    self.end_col == other.end_col)
        return False


    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, col):
        return self.cols_to_file[col] + self.rows_to_ranks[row]