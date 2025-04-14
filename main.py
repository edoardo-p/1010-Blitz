import pygame
import torch
from matplotlib import pyplot as plt

from backend.agent import DQNAgent
from backend.custom_env import Game1010, State
from frontend import WIN_HEIGHT, WIN_WIDTH, gui

MODEL_DIR = r"backend\models\embed_cnn"
EPOCHS = 1000
TAU = 0.005

PIECE_HASH_TO_IDX = {
    -8458139203682520985: 0,
    3452360341691682072: 1,
    7030254474778767472: 2,
    -84101060784792413: 3,
    -2034599508365314973: 4,
    6339438634532413599: 5,
    13544252848704378161: 6,
    -13622761056297464961: 7,
    -11047246991494576689: 8,
    -6361720192145132613: 9,
    -3786206127342244341: 10,
    -15573259503877987521: 11,
    -5248722913399736389: 12,
    -7833123586460155273: 13,
    2491413004018095859: 14,
    -3682918490356578883: 15,
    7810842028847436259: 16,
    1947204692514697561: 17,
    13440965211718712703: 18,
}


def squares_to_idx(squares: list[tuple[int, int]]) -> int:
    hash_sum = sum(hash(tuple(square)) for square in squares)
    return PIECE_HASH_TO_IDX[hash_sum]


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
        agent.step = epoch

        while True:
            if render:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return scores

            action = agent.choose_action(*state)
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
    agent.train = False

    while True:
        action = agent.choose_action(*state)
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
    render, to_train = True, True

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
        train=to_train,
    )

    if to_train:
        scores = train(env, agent, device, screen)
        plt.plot(scores)
        plt.show()

    test(env, agent, device, screen)


if __name__ == "__main__":
    main()
