#!/usr/bin/env python3
# this script was mostly written by ChatGPT

import chess
import chess.engine

STOCKFISH_PATH = "./stockfish"

def str_board_fancy(board):
    from_chars = "KQRBNPkqrbnp"
    to_chars = "♔♕♖♗♘♙♚♛♜♝♞p"
    txt = str(board)
    for from_char, to_char in zip(from_chars, to_chars):
        txt = txt.replace(from_char, to_char)
    return txt

def main():
    board = chess.Board()

    with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
        print("Welcome to Trumpfish")

        while not board.is_game_over():
            print(str_board_fancy(board))

            move_uci = input("\nYour move (in UCI, e.g., e2e4): ").strip()
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

            result = engine.play(board, chess.engine.Limit(time=0.5))
            board.push(result.move)
            print(f"\nTrumpfish plays: {result.move}")

        print("\nGame over:", board.result())

if __name__ == "__main__":
    main()
