import pygame as p

from Chess import ChessEngine, SmartMoveFinder

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15

IMAGES = {}

'''
load_images() is used for mapping string key of piece to image to put it into the IMAGES dictionary'''

def load_images():
    pieces = ["wp", "wN", "wB", "wR", "wQ", "wK", "bp", "bN", "bB", "bR", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.game_state()
    valid_moves = gs.get_valid_moves()
    move_made = False
    load_images()
    running = True
    sq_selected = ()
    player_clicks = []
    player_one = True # If a Human is playing white, then this will be True. If an AI is playing, then False.
    player_two = False # Human playing black
    
    while running:
        human_turn = (gs.white_to_move and player_one) or (not gs.white_to_move and player_two)
        
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gs.checkmate and not gs.stalemate and human_turn:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sq_selected == (row, col):
                        sq_selected = ()
                        player_clicks = []
                    else:
                        sq_selected = (row, col)
                        player_clicks.append(sq_selected)
                    if len(player_clicks) == 2:
                        move = ChessEngine.move(player_clicks[0], player_clicks[1], gs.board)
                        print(move.get_chess_notation())
                        if move in valid_moves:
                            gs.make_move(move)
                            move_made = True
                        sq_selected = ()
                        player_clicks = []
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undo_move()
                    move_made = True
        
        # AI move finder
        if not gs.checkmate and not gs.stalemate and not human_turn:
            ai_move = SmartMoveFinder.find_best_move(gs, valid_moves)
            if ai_move is None:
                ai_move = SmartMoveFinder.find_random_move(valid_moves)
            gs.make_move(ai_move)
            move_made = True
            
        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False

        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

'''draw_state, is used for drawing the board and putting pieces into it '''
def draw_game_state(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)

def draw_board(screen):
    colors = [p.Color("white"), p.Color("pink")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], (c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()






