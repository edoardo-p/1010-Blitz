import json
import random

import pygame
from board import Board
from constants import GRID_HEIGHT, GRID_X, GRID_Y, TILE_SIZE, WIN_HEIGHT, WIN_WIDTH
from grid import Grid
from piece import Piece

with open(r"frontend\vectors.json", "r") as f:
    piece_vectors = json.load(f)
del f


def draw_piece_menu(
    pieces: list[Piece], draw_mask: list[bool], screen: pygame.surface.Surface
):
    for i, (piece, to_draw) in enumerate(zip(pieces, draw_mask)):
        if not to_draw:
            continue
        piece.update(WIN_WIDTH * i // 3 + TILE_SIZE * 2, GRID_HEIGHT + TILE_SIZE * 4)
        piece.show(0.5, screen)


def generatePieces() -> list[Piece]:
    pieces = []
    for _ in range(3):
        piece = random.choice(piece_vectors)
        pieces.append(Piece(piece["pos"], pygame.Color(piece["color"])))

    return pieces


def convert(x: int, y: int) -> tuple[int, int]:
    new_x = (x - GRID_X) // TILE_SIZE
    new_y = (y - GRID_Y) // TILE_SIZE
    return new_x, new_y


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    board = Board()
    grid = Grid(GRID_X, GRID_Y)
    is_holding = False
    pieces = generatePieces()
    available_slots = [True, True, True]
    score = 0

    while True:
        screen.fill(0)
        board.show(score, screen)
        grid.show(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN and not is_holding:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if GRID_HEIGHT + GRID_Y <= mouse_y <= WIN_HEIGHT:
                    slot = 3 * mouse_x // WIN_WIDTH
                    if available_slots[slot]:
                        piece = pieces[slot]
                        available_slots[slot] = False
                        is_holding = True

            elif event.type == pygame.MOUSEBUTTONDOWN and is_holding:
                x, y = convert(*pygame.mouse.get_pos())
                score_delta = grid.update(y, x, piece)
                if score_delta:
                    score += score_delta

                    if not any(available_slots):
                        pieces = generatePieces()
                        available_slots = [True, True, True]

                    if grid.has_lost(pieces):
                        print("You lost!")
                        draw_piece_menu(pieces, available_slots, screen)
                        grid.update(x, y, piece)
                        grid.show(screen)

                    is_holding = False

        if is_holding:
            piece.update(*pygame.mouse.get_pos())
            piece.show(1, screen)

        draw_piece_menu(pieces, available_slots, screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()
