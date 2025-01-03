#For checking specific moves for a piece

class Valid_Moves:
    @staticmethod
    def check_pawn(board, coords, player):
        piece_color = board[coords[0]][coords[1]][0]
        if player == piece_color:
            if coords[0] == 6:
                if board[coords[0] - 1][coords[1]] == '--':
                    return [(coords[0] - 1, coords[1]), (coords[0] - 2, coords[1])]
                else:
                    return [(coords[0] - 1, coords[1])]
        else:
            pass
    
    @staticmethod
    def check_knight(board, coords, player):
        pass
    
    @staticmethod
    def check_king(board, coords, player):
        pass

    @staticmethod
    def check_queen(board, coords, player):
        pass

    @staticmethod
    def check_rook(board, coords, player):
        pass

    @staticmethod
    def check_bishop(board, coords, player):
        pass