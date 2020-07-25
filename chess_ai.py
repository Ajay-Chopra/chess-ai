import chess
import chess.svg
import piece_square_tables
import sys

def evaluate_board(board):
    '''
    Given a board, evaluate the board state based on piece-square tables
    '''
    if board.is_checkmate():
        if board.turn:
            return 9999
        else:
            return -9999
    elif board.is_stalemate() or board.is_insufficient_material():
        return 0
    else:
        # First, calculate total material on board
        white_pawns = len(board.pieces(chess.PAWN, chess.WHITE)) # Number of white pawns on board
        black_pawns = len(board.pieces(chess.PAWN, chess.BLACK))
        white_knights = len(board.pieces(chess.KNIGHT, chess.WHITE))
        black_knights = len(board.pieces(chess.KNIGHT, chess.BLACK))
        white_bishops = len(board.pieces(chess.BISHOP, chess.WHITE))
        black_bishops = len(board.pieces(chess.BISHOP, chess.BLACK))
        white_rooks = len(board.pieces(chess.ROOK, chess.WHITE))
        black_rooks = len(board.pieces(chess.ROOK, chess.BLACK))
        white_queen = len(board.pieces(chess.QUEEN, chess.WHITE))
        black_queen = len(board.pieces(chess.QUEEN, chess.BLACK))
        white_king = len(board.pieces(chess.KING, chess.WHITE))
        black_king = len(board.pieces(chess.KING, chess.BLACK))

        # Calc material value using weights given here: https://www.chessprogramming.org/Simplified_Evaluation_Function
        total_material = (100*(white_pawns - black_pawns) + 320*(white_knights - black_knights)
                        + 330*(white_bishops - black_bishops) + 500*(white_rooks - black_rooks)
                        + 900*(white_queen - black_queen))

        # Calculate the positional values of the pieces using piece-square tables
        pawn_table = piece_square_tables.pawn_ps
        knight_table = piece_square_tables.knight_ps
        bishop_table = piece_square_tables.bishop_ps
        rook_table = piece_square_tables.rook_ps
        queen_table = piece_square_tables.queen_ps

        pawn_pos_val = (sum(pawn_table[i] for i in board.pieces(chess.PAWN, chess.WHITE))
                       + sum(-pawn_table[chess.square_mirror(i)] for i in board.pieces(chess.PAWN, chess.BLACK)))

        knight_pos_val = (sum(knight_table[i] for i in board.pieces(chess.KNIGHT, chess.WHITE))
                       + sum(-knight_table[chess.square_mirror(i)] for i in board.pieces(chess.KNIGHT, chess.BLACK)))

        bishop_pos_val = (sum(bishop_table[i] for i in board.pieces(chess.BISHOP, chess.WHITE))
                       + sum(-bishop_table[chess.square_mirror(i)] for i in board.pieces(chess.BISHOP, chess.BLACK)))

        rook_pos_val = (sum(rook_table[i] for i in board.pieces(chess.ROOK, chess.WHITE))
                       + sum(-rook_table[chess.square_mirror(i)] for i in board.pieces(chess.ROOK, chess.BLACK)))

        queen_pos_val = (sum(queen_table[i] for i in board.pieces(chess.QUEEN, chess.WHITE))
                       + sum(-queen_table[chess.square_mirror(i)] for i in board.pieces(chess.QUEEN, chess.BLACK)))

        total_board_val = (total_material + pawn_pos_val + knight_pos_val + bishop_pos_val
                          + rook_pos_val + queen_pos_val)

        if board.turn:
            return total_board_val
        else:
            return -total_board_val



def minimax(board, depth, alpha, beta, maximizingPlayer):
    '''
    Perform depth first search of possible moves to find the best move
    Use alpha-beta pruning to delete extraenous branches to reduce search time
    '''
    if depth == 0 or board.is_game_over():
        return evaluate_board(board), chess.Move.null()
    elif maximizingPlayer:
        max_val = -10000
        best_move = None
        for move in board.legal_moves:
            board.push(move)
            child_val, move_made = minimax(board, depth - 1, alpha, beta, maximizingPlayer = False)
            board.pop()
            if child_val > max_val:
                max_val = child_val
                best_move = move
            alpha = max(alpha, child_val)
            if beta <= alpha:
                break
        return max_val, best_move
    else:
        min_val = 10000
        best_move = None
        for move in board.legal_moves:
            board.push(move)
            child_val, move_made = minimax(board, depth - 1, alpha, beta, maximizingPlayer = True)
            board.pop()
            if child_val < min_val:
                min_val = child_val
                best_move = move
            beta = min(beta, child_val)
            if beta <= alpha:
                break
        return min_val, best_move



def make_ai_move(board):
    '''
    AI calculates maximizing move and pushes it to the board
    '''
    optimum_val, move = minimax(board, 3, -10000, 10000, True)
    board.push(move)




def run_game():
    '''
    Run the game with a fresh board
    '''
    print("WELCOME TO CHESS")
    print("---------------------------------------------------------------------")
    print("Enter moves in the form: r1f1r2f2")
    print("For example if you wanted to move from F2 to F3 you would type f2f3")
    print("---------------------------------------------------------------------")
    board = chess.Board()
    print(board)
    print("---------------------------------------------------------------------")
    while True:
        print("Please enter a move. Type DONE when finished")
        for line in sys.stdin:
            if line.strip() == 'DONE':
                break
            elif len(line.strip()) != 4:
                print("This is an incorrenct format")
                print("Enter moves in the form: r1f1r2f2")
            else:
                human_move = chess.Move.from_uci(line.strip())
                if human_move in board.legal_moves:
                    board.push(human_move)
                    print("-----------------------------------------------------")
                    print(board)
                    print("-----------------------------------------------------")
                    print("AI is making its move....")
                    make_ai_move(board)
                    print("-----------------------------------------------------")
                    print(board)
                    print("-----------------------------------------------------")
                    break
                else:
                    print("This is not a legal move")


run_game()
