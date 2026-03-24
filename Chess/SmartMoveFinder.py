import random
from Chess.MLEvaluator import init_model, evaluate_board_ml, TORCH_AVAILABLE

piece_score = {"K": 0, "Q": 1000, "R": 500, "B": 300, "N": 300, "p": 100}
CHECKMATE = 100000
STALEMATE = 0
DEPTH = 3

next_move = None
counter = 0

USE_ML_EVALUATION = init_model() # Tries to initialize PyTorch ML model


def find_random_move(valid_moves):
    return random.choice(valid_moves)

def find_best_move(gs, valid_moves):
    global next_move, counter
    next_move = None
    counter = 0
    random.shuffle(valid_moves) # Add randomness so it doesn't always play same moves
    find_move_nega_max_alpha_beta(gs, valid_moves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.white_to_move else -1)
    print("Positions evaluated:", counter)
    return next_move

def find_move_nega_max_alpha_beta(gs, valid_moves, depth, alpha, beta, turn_multiplier):
    global next_move, counter
    counter += 1
    if depth == 0:
        return turn_multiplier * score_board(gs)
        
    # Move ordering could be added here to improve alpha-beta pruning efficiency
    
    max_score = -CHECKMATE
    for move in valid_moves:
        gs.make_move(move)
        next_moves = gs.get_valid_moves()
        if gs.checkmate:
            score = CHECKMATE
        elif gs.stalemate:
            score = STALEMATE
        else:
            score = -find_move_nega_max_alpha_beta(gs, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        gs.undo_move()
        
        if max_score > alpha: # Pruning
            alpha = max_score
        if alpha >= beta:
            break
            
    return max_score

def score_board(gs):
    """
    Score the board based on material.
    A positive score is good for white, a negative score is good for black.
    """
    if gs.checkmate:
        if gs.white_to_move:
            return -CHECKMATE # black wins
        else:
            return CHECKMATE # white wins
    elif gs.stalemate:
        return STALEMATE
        
    if USE_ML_EVALUATION:
        return evaluate_board_ml(gs.board)
        
    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += piece_score[square[1]]
            elif square[0] == 'b':
                score -= piece_score[square[1]]
    return score
