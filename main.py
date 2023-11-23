import pygame

from backend.game import Game
from frontend import GRID_HEIGHT, GRID_X, GRID_Y, TILE_SIZE, WIN_HEIGHT, WIN_WIDTH, gui


def convert(x: int, y: int) -> tuple[int, int]:
    col = (x - GRID_X) // TILE_SIZE
    row = (y - GRID_Y) // TILE_SIZE
    return row, col


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    game = Game(board_size=10)
    is_holding = False

    while True:
        screen.fill(0)
        gui.draw_game(screen, game)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN and not is_holding:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if GRID_HEIGHT + GRID_Y <= mouse_y <= WIN_HEIGHT:
                    piece = game.get_piece_at_slot(3 * mouse_x // WIN_WIDTH)
                    if piece:
                        is_holding = True

            elif event.type == pygame.MOUSEBUTTONDOWN and is_holding:
                row, col = convert(*pygame.mouse.get_pos())
                if game.update(row, col, piece):
                    if game.has_lost():
                        pygame.quit()
                        print(f"Final score: {game.score}")
                        return

                    is_holding = False

        if is_holding:
            piece.update(*pygame.mouse.get_pos())
            gui.draw_piece(screen, piece)

        gui.draw_piece_menu(screen, game.pieces)
        pygame.display.flip()


if __name__ == "__main__":
    main()
