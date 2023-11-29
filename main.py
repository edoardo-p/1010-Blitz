import pygame

from backend.agent import Agent
from backend.custom_env import Game1010
from frontend import GRID_X, GRID_Y, TILE_SIZE, WIN_HEIGHT, WIN_WIDTH, gui

EPOCHS = 10


def convert(x: int, y: int) -> tuple[int, int]:
    col = (x - GRID_X) // TILE_SIZE
    row = (y - GRID_Y) // TILE_SIZE
    return row, col


def update_gui(screen: pygame.Surface, env: Game1010):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill(0)
        gui.draw_game(screen, env)
        pygame.display.flip()


def main():
    render = True

    if render:
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    env = Game1010()
    agent = Agent(env.board_size * env.board_size * env.max_pieces, (10, 10))

    for epoch in range(1, EPOCHS + 1):
        state = env.reset()
        step_count = 0
        total_reward = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            action = agent.choose_action(state, random_choice=True)
            piece_idx, coords = divmod(action, env.board_size**2)
            row, col = divmod(coords, env.board_size)
            next_state, reward, done = env.step(piece_idx, row, col)
            # agent.learn()

            if done:
                break

            if render:
                screen.fill(0)
                gui.draw_game(screen, env)
                pygame.display.flip()
                clock.tick(60)

            state = next_state
            step_count += 1
            total_reward += reward

        print(f"Epoch: {epoch}, Score: {env.score}")

    env.close()


if __name__ == "__main__":
    main()
