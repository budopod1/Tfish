#!/usr/bin/env python3
# this script originally partially written by ChatGPT

import chess
import chess.engine
import random

RIGHT_REMOVAL_CHANCE = 0.1
DEPORTATION_CHANCE = 0.25

STOCKFISH_PATH = "./stockfish"

def str_board_fancy(board):
    from_chars = "KQRBNPkqrbnp"
    to_chars = "♔♕♖♗♘♙♚♛♜♝♞p"
    txt = str(board)
    for from_char, to_char in zip(from_chars, to_chars):
        txt = txt.replace(from_char, to_char)
    txt = "\n".join(
        f"{line} {8-i}"
        for i, line in enumerate(txt.split("\n"))
    )
    txt += "\n" + " ".join("abcdefgh")
    return txt

def do_human_move(board):
    while True:
        move_uci = input("\nYour move (in UCI): ").strip()
        try:
            move = chess.Move.from_uci(move_uci)
            if move in board.legal_moves:
                board.push(move)
            else:
                print("Illegal move.")
                continue
        except:
            print("Invalid input.")
            continue
        break

def do_engine_move(board):
    if random.random() < RIGHT_REMOVAL_CHANCE and not board.is_check():
        castling_squares = (chess.BB_A8 | chess.BB_H8)
        if board.castling_rights & castling_squares:
            board.castling_rights &= ~castling_squares
            board.turn = chess.BLACK
            print("Uh, oh! Trumpfish revoked your rooks castling rights")
            return

    if random.random() < DEPORTATION_CHANCE and not board.is_check():
        chosen_piece = random.choice([
            chess.PAWN,
            chess.KNIGHT,
            chess.BISHOP,
            chess.ROOK
        ])
        piece_squares = board.pieces(chosen_piece, chess.BLACK)
        if piece_squares:
            piece_square = random.choice(list(piece_squares))
            board.remove_piece_at(piece_square)
            board.turn = chess.BLACK
            print(f"Uh, oh! Trumpfish deported your piece at {chess.square_name(piece_square)}")
            return
    
    board.clear_stack()

    with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
        result = engine.play(board, chess.engine.Limit(time=0.5))
        board.push(result.move)
    
    print(f"\nTrumpfish plays: {result.move}")

def main():
    board = chess.Board()

    print("Welcome to Trumpfish")

    while True:
        do_engine_move(board)
        if board.is_game_over():
            break
        
        print(str_board_fancy(board))

        do_human_move(board)
        if board.is_game_over():
            break

    print("\nGame over:", board.result())

if __name__ == "__main__":
    main()
