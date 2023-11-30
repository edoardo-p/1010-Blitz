from itertools import count

import pygame

from backend.agent import DQNAgent
from backend.custom_env import Game1010
from frontend import GRID_X, GRID_Y, TILE_SIZE, WIN_HEIGHT, WIN_WIDTH, gui

EPOCHS = 500
TAU = 0.005


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

    env = Game1010(max_pieces=1)
    agent = DQNAgent(env.board_size * env.board_size * env.max_pieces, (10, 10))

    for epoch in range(1, EPOCHS + 1):
        state = env.reset()
        total_reward = 0

        for step in count():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            piece_idx, row, col = agent.choose_action(state, step, random_choice=True)
            next_state, reward, done = env.step(piece_idx, row, col)

            if done:
                agent.memory.push(state, (piece_idx, row, col), None, reward)
                break

            agent.memory.push(state, (piece_idx, row, col), next_state, reward)
            state = next_state
            agent.learn()

            # Soft update of the target network's weights
            # θ′ ← τ θ + (1 −τ )θ′
            target_net_state_dict = agent.target_net.state_dict()
            policy_net_state_dict = agent.policy_net.state_dict()
            for key in policy_net_state_dict:
                target_net_state_dict[key] = policy_net_state_dict[
                    key
                ] * TAU + target_net_state_dict[key] * (1 - TAU)
            agent.target_net.load_state_dict(target_net_state_dict)

            if render:
                screen.fill(0)
                gui.draw_game(screen, env)
                pygame.display.flip()
                clock.tick(60)

            total_reward += reward

        print(f"Epoch: {epoch}, Score: {env.score}")

    env.close()


if __name__ == "__main__":
    main()
