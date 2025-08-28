## 1010 Blitz: Game & Reinforcement Learning AI

### Overview

This repository contains an implementation of the classic 1010 puzzle game, featuring a graphical interface and a reinforcement learning (RL) agent designed to play the game autonomously. The project is structured with a clear separation between game logic, user interface, and AI components.

---

### Current Status

- **Game Implementation:**  
  The 1010 game is fully playable with a UI built using `pygame` for RL integration. Core mechanics closely match the original game, including piece placement, line clearing, and scoring.

- **Reinforcement Learning Model:**  
  The repository includes a Deep Q-Network (DQN) agent implemented in PyTorch. The agent interacts with a custom environment (`Game1010`) and learns to play by maximizing score through trial and error.

  - The RL agent uses a convolutional neural network to process the board state and an embedding layer for piece representation.
  - Experience replay and target network updates are implemented for stable training.
  - The agent can be trained and tested using provided scripts, with model checkpoints saved for later evaluation.

- **Training & Testing:**
  - Training and evaluation scripts are provided in `main.py`.
  - The agent can be trained to play the game, and its performance can be visualized.
  - Pre-trained model weights are included in the repository.

---

### Features

- **Game Mechanics:**

  - 10x10 grid, scoreboard, timer, and next pieces display.
  - Click to place pieces, with validity checks for moves.
  - Spacebar returns held pieces to the next box.
  - Automatic line clearing and scoring.

- **RL Agent:**

  - Deep Q-Network with CNN and embedding layers.
  - Learns to maximize score and survive longer in blitz mode.
  - Can be trained or tested via command-line options.

### How to Run

1. **Install dependencies:**

   - Python 3.10+, PyTorch, pygame, matplotlib, gymnasium, scipy.

2. **Train the RL agent:**  
   Set `TRAIN = True` in `main.py` and run:

   ```
   python main.py
   ```

3. **Test the RL agent:**  
   Set `TRAIN = False` and run:

   ```
   python main.py
   ```

4. **Play manually:**  
   Use the UI to interact with the game.

---

### Known Issues

- Piece snapping at the bottom may not return to the original location.
- If a losing move clears lines, the score updates but the grid may not refresh correctly.
- RL agent performance is limited by training time and reward design.

---

### Repository Structure

- `backend/` – Game logic, RL agent, environment, models.
- `frontend/` – UI components.
- `train.py` – Entry point for training.
- `test.py` – Entry point for testing.
- `README.md` – Project documentation.

---

### Credits

Developed as a learning project to combine game development and reinforcement learning.
