import chess
import chess.svg
import piece_square_tables as pst
import sys

def init_board_value(board):
    '''
    Evaluates value of the starting board using piece squares tables and
    weights assigned to each piece type
    '''
    global board_value
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
    pawn_table = pst.pawn_ps
    knight_table = pst.knight_ps
    bishop_table = pst.bishop_ps
    rook_table = pst.rook_ps
    queen_table = pst.queen_ps

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

    board_value = (total_material + pawn_pos_val + knight_pos_val + bishop_pos_val
                      + rook_pos_val + queen_pos_val)

    return board_value


def evaluate_board(board):
    '''
    Evaluate any given board
    First check for checkmate or stalement. If neither condition is true
    return the value of the board from the current value of the global variable
    '''
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    if board.is_stalemate():
        return 0

    if board.is_insufficient_material():
        return 0

    eval = board_value
    if board.turn:
        return eval
    else:
        return -eval

def update_board_val(piecetypes, tables, piecevalues, move, turn, board):
    '''
    Given a move, update the global board_value
    '''
    global board_value
    # Update based on piecesquare tables
    piece = board.piece_type_at(move.from_square)
    # Subtract value of square that piece move from
    if turn:
        board_value -= tables[piece - 1][move.from_square]
        # Handle castling
        if (move.from_square == chess.E1) and (move.to_square == chess.G1):
            board_value -= tables[3][chess.H1]
            board_value += tables[3][chess.F1]
        elif (move.from_square == chess.E1) and (move.to_square == chess.C1):
            board_value -= tables[3][chess.A1]
            board_value += tables[3][chess.D1]
    else:
        board_value = board_value + tables[piece - 1][move.from_square]
        # Handle castling
        if (move.from_square == chess.E8) and (move.to_square == chess.G8):
            board_value -= tables[3][chess.H8]
            board_value += tables[3][chess.F8]
        elif (move.from_square == chess.E8) and (move.to_square == chess.C8):
            board_value -= tables[3][chess.A8]
            board_value += tables[3][chess.D8]

    # Add value of square that piece is moving to

    if turn:
        board_value += tables[piece - 1][move.to_square]
    else:
        board_value -= tables[piece - 1][move.to_square]

    # Update material value
    if move.drop != None:
        if turn:
            board_value += piecevalues[move.drop - 1]
        else:
            board_value -= piecevalues[move.drop - 1]
    
    # Update promotion
    if move.promotion != None:
        if turn:
            board_value += piecevalues[move.promotion - 1] - piecevalues[piece - 1]
            board_value -= (tables[piece - 1][move.to_square] 
                + tables[move.promotion - 1][move.to_square])
        else:
            board_value -= piecevalues[move.promotion-1] + piecevalues[piece-1]
            board_value += (tables[piece - 1][move.to_square]
                - tables[move.promotion - 1][move.to_square])
    
    return move

def make_move(board, move):
    update_board_val(
        piecetypes = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING],
        tables = [pst.pawn_ps, pst.knight_ps, pst.bishop_ps, pst.rook_ps, pst.queen_ps, pst.king_middle_ps],
        piecevalues = [100,320,330,500,900],
        move = move,
        turn = board.turn,
        board = board
        )
    
    board.push(move)
    return move
    

def unmake_move(board):
    move = board.pop()
    update_board_val(
        piecetypes = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING],
        tables = [pst.pawn_ps, pst.knight_ps, pst.bishop_ps, pst.rook_ps, pst.queen_ps, pst.king_middle_ps],
        piecevalues = [100,320,330,500,900],
        move = move,
        turn = not board.turn,
        board = board
    )
    return move
    
def minimax(board, depth, alpha, beta, maximizingPlayer):
    '''
    Perform depth first search of possible moves to find the best move
    Use alpha-beta pruning to delete extraenous branches to reduce search time
    '''
    if depth == 0 or board.is_game_over():
        return quiet_search(board, alpha, beta), chess.Move.null()
    elif maximizingPlayer:
        max_val = -10000
        best_move = None
        for move in board.legal_moves:
            make_move(board, move)
            child_val, move_made = minimax(board, depth - 1, alpha, beta, maximizingPlayer = False)
            unmake_move(board)
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
            make_move(board, move)
            child_val, move_made = minimax(board, depth - 1, alpha, beta, maximizingPlayer = True)
            unmake_move(board)
            if child_val < min_val:
                min_val = child_val
                best_move = move
            beta = min(beta, child_val)
            if beta <= alpha:
                break
        return min_val, best_move


def quiet_search(board, alpha, beta):
    '''
    Perform a depth first search of all capture moves
    '''
    stand_pat = evaluate_board(board)
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            make_move(board, move)
            score = -quiet_search(board, -alpha, -beta)
            unmake_move(board)

            if (score >= beta):
                return beta

            if (score > alpha):
                alpha = score
    return alpha

def make_ai_move(board):
    '''
    AI calculates maximizing move and pushes it to the board
    '''
    optimum_val, move = minimax(board, 3, -10000, 10000, True)
    board.push(move)


def run_game():
    print("WELCOME TO CHESS")
    print("---------------------------------------------------------------------")
    print("Enter moves in the form: r1f1r2f2")
    print("For example if you wanted to move from F2 to F3 you would type f2f3")
    print("---------------------------------------------------------------------")
    board = chess.Board()
    init_board_value(board)
    print(board)
    print("---------------------------------------------------------------------")
    while True:
        print("Please enter a move. Press ENTER when finished")
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





