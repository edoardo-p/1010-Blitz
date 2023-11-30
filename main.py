from itertools import count

import pygame
import torch
from matplotlib import pyplot as plt

from backend.agent import DQNAgent
from backend.custom_env import Game1010
from backend.tile import Tile
from frontend import WIN_HEIGHT, WIN_WIDTH, gui

EPOCHS = 10
TAU = 0.005


def state_to_tensor(state: list[list[Tile]], device: torch.device) -> torch.Tensor:
    return (
        torch.tensor(
            [not tile.empty for row in state for tile in row],
            dtype=torch.float32,
        )
        .unsqueeze(0)
        .to(device)
    )


def main():
    render = True

    if render:
        pygame.init()
        screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    model_dir = r"backend\models\linear_test"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    env = Game1010(max_pieces=1)
    agent = DQNAgent(
        env.board_size * env.board_size * env.max_pieces,
        (env.board_size, env.board_size),
        device,
    )
    scores = []

    for epoch in range(1, EPOCHS + 1):
        state = state_to_tensor(env.reset(), device)

        for step in count():
            if render:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

            action = agent.choose_action(state, step)
            observation, reward, done = env.step(*agent.action_to_tuple(action))
            reward = torch.tensor(reward, dtype=torch.float32).unsqueeze(0).to(device)

            if done:
                agent.memory.push(state, action, None, reward)
                break

            next_state = state_to_tensor(observation, device)
            agent.memory.push(state, action, (next_state), reward)
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
                agent.policy_net.state_dict(), rf"{model_dir}\policy_net_{epoch}.pth"
            )
            torch.save(
                agent.target_net.state_dict(), rf"{model_dir}\target_net_{epoch}.pth"
            )
        scores.append(env.score)
        print(f"Epoch: {epoch}, Score: {env.score}")

    plt.plot(scores)
    plt.show()


if __name__ == "__main__":
    main()
