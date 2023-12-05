import pygame
import torch
from matplotlib import pyplot as plt

from backend.agent import DQNAgent
from backend.custom_env import Game1010, State
from frontend import WIN_HEIGHT, WIN_WIDTH, gui

MODEL_DIR = r"backend\models\embed_cnn"
EPOCHS = 1000
TAU = 0.005

PIECE_TO_IDX = {
    (1, 0, 0): 0,
    (4, -2, -2): 1,
    (9, 0, 0): 2,
    (2, 0, -1): 3,
    (3, 0, 0): 4,
    (4, 0, -2): 5,
    (5, 0, 0): 6,
    (2, 1, 0): 7,
    (3, 0, 0): 8,
    (4, 2, 0): 9,
    (5, 0, 0): 10,
    (3, 1, 1): 11,
    (3, 1, -1): 12,
    (3, -1, 1): 13,
    (3, -1, -1): 14,
    (5, 3, 3): 15,
    (5, 3, -3): 16,
    (5, -3, 3): 17,
    (5, -3, -3): 18,
}


def squares_to_idx(squares: list[tuple[int, int]]) -> int:
    x_sum = sum(square[0] for square in squares)
    y_sum = sum(square[1] for square in squares)
    return PIECE_TO_IDX[(len(squares), x_sum, y_sum)]  # type: ignore


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
        torch.tensor(squares_to_idx(piece.squares_pos), dtype=torch.int)
        .unsqueeze(0)
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

        while True:
            if render:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return scores

            action = agent.choose_action(*state, epoch)
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

        if epoch % 500 == 0:
            torch.save(agent.policy_net.state_dict(), rf"{MODEL_DIR}\policy_net.pth")
            torch.save(agent.target_net.state_dict(), rf"{MODEL_DIR}\target_net.pth")

        scores.append(env.score)
        print(f"Epoch: {epoch}, Score: {env.score}")

    return scores


def test(
    env: Game1010,
    agent: DQNAgent,
    device: torch.device,
    screen: pygame.Surface | None = None,
):
    render = screen is not None
    state = state_to_tensor(env.reset(), device)
    agent.load(MODEL_DIR)

    while True:
        action = agent.choose_action(*state, 999999)
        observation, _, done = env.step(*agent.action_to_tuple(action))

        if done:
            print(f"Final score: {env.score}")
            break

        next_state = state_to_tensor(observation, device)
        state = next_state

        if render:
            screen.fill(0)
            gui.draw_game(screen, env)
            pygame.display.flip()

    if render:
        pygame.quit()


def main():
    render, to_train = False, True

    screen = None
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

    if to_train:
        scores = train(env, agent, device, screen)
        plt.plot(scores)
        plt.show()

    test(env, agent, device, screen)


if __name__ == "__main__":
    main()
