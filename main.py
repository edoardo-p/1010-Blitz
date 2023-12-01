from itertools import count

import pygame
import torch
from matplotlib import pyplot as plt

from backend.agent import DQNAgent
from backend.custom_env import Game1010, State
from frontend import WIN_HEIGHT, WIN_WIDTH, gui

MODEL_DIR = r"backend\models\cnn"
EPOCHS = 10
TAU = 0.005


def squares_to_grid(squares: list[tuple[int, int]]) -> list[list[int]]:
    grid = [[0] * 5 for _ in range(5)]
    for square in squares:
        grid[2 + square[0]][2 + square[1]] = 1
    return grid


def state_to_tensor(
    state: State, device: torch.device
) -> tuple[torch.Tensor, torch.Tensor]:
    grid, piece = state
    return (
        torch.tensor(
            [not tile.empty for row in grid for tile in row],
            dtype=torch.float32,
        )
        .reshape(-1, 1, 10, 10)
        .to(device),
        torch.tensor(squares_to_grid(piece.squares_pos), dtype=torch.float32)
        .reshape(-1, 1, 5, 5)
        .to(device),
    )


def train(
    env: Game1010,
    agent: DQNAgent,
    device: torch.device,
    screen: pygame.Surface | None = None,
) -> list[int]:
    scores = []
    render = screen is not None

    for epoch in range(1, EPOCHS + 1):
        state = state_to_tensor(env.reset(), device)

        for step in count():
            if render:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return scores

            action = agent.choose_action(*state, step)
            observation, reward, done = env.step(*agent.action_to_tuple(action))
            reward = torch.tensor(reward, dtype=torch.float32).unsqueeze(0).to(device)

            if done:
                agent.memory.push(state, action, None, reward)
                break

            next_state = state_to_tensor(observation, device)
            agent.memory.push(state, action, next_state, reward)
            state = next_state
            agent.learn()

            # Soft update of the target network's weights
            # θ′ ← τθ + (1 − τ)θ′
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

        if epoch % 200 == -1:
            torch.save(
                agent.policy_net.state_dict(), rf"{MODEL_DIR}\policy_net_{epoch}.pth"
            )
            torch.save(
                agent.target_net.state_dict(), rf"{MODEL_DIR}\target_net_{epoch}.pth"
            )

        scores.append(env.score)
        print(f"Epoch: {epoch}, Score: {env.score}")

    if render:
        pygame.quit()

    return scores


def main():
    screen, render = None, False

    if render:
        pygame.init()
        screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    env = Game1010(max_pieces=1)
    agent = DQNAgent(
        env.board_size * env.board_size * env.max_pieces,
        (env.board_size, env.board_size),
        device,
    )

    scores = train(env, agent, device, screen)
    plt.plot(scores)
    plt.show()


if __name__ == "__main__":
    main()
