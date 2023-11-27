import gymnasium as gym


gym.register(
    id="custom_env/Game1010-v0",
    entry_point="backend.custom_env:Game1010",
    nondeterministic=True,
    kwargs={"board_size": 10},
)
