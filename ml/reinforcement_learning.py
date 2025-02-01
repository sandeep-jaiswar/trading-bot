import gym
import numpy as np
import pandas as pd
from stable_baselines3 import DQN
from gym import spaces
from sklearn.preprocessing import MinMaxScaler
import random

class TradingEnv(gym.Env):
    """Custom Reinforcement Learning Trading Environment"""
    
    def __init__(self, df, initial_balance=10000):
        super(TradingEnv, self).__init__()

        self.df = df.reset_index(drop=True)
        self.initial_balance = initial_balance
        self.current_step = 0
        self.balance = initial_balance
        self.position = 0  # 1 = Long, -1 = Short, 0 = No position
        self.entry_price = 0

        self.scaler = MinMaxScaler()
        self.df.iloc[:, 1:] = self.scaler.fit_transform(self.df.iloc[:, 1:])  # Scale indicators

        self.action_space = spaces.Discrete(3)  # 0 = Hold, 1 = Buy, 2 = Sell
        self.observation_space = spaces.Box(low=0, high=1, shape=(len(self.df.columns),), dtype=np.float32)

    def reset(self):
        """Reset environment for a new episode"""
        self.current_step = 0
        self.balance = self.initial_balance
        self.position = 0
        self.entry_price = 0
        return self._next_observation()

    def _next_observation(self):
        """Get the next state (market data)"""
        obs = self.df.iloc[self.current_step].values
        # Convert Timestamp to a numerical value
        obs[0] = pd.to_datetime(obs[0]).timestamp()  # Assuming the first column is the date
        return np.array(obs, dtype=np.float32)

    def step(self, action):
        """Execute an action in the environment"""
        self.current_step += 1
        current_price = self.df.iloc[self.current_step]["close"]

        reward = 0
        done = self.current_step >= len(self.df) - 1

        if action == 1:  # Buy
            if self.position == 0:
                self.position = 1
                self.entry_price = current_price
        elif action == 2:  # Sell
            if self.position == 1:
                reward = (current_price - self.entry_price) * 100  # Profit
                self.balance += reward
                self.position = 0

        return self._next_observation(), reward, done, {}

    def render(self, mode="human"):
        """Render trading environment"""
        print(f"Step: {self.current_step}, Balance: {self.balance}, Position: {self.position}")

# Train RL Agent
def train_rl_agent(df):
    env = TradingEnv(df)
    model = DQN("MlpPolicy", env, verbose=1, learning_rate=0.001, buffer_size=50000)
    model.learn(total_timesteps=100000)
    model.save("ml/rl_trading_model")
    return model

# Predict using RL Agent
def predict_trade(df):
    env = TradingEnv(df)
    model = DQN.load("ml/rl_trading_model")

    obs = env.reset()
    done = False
    while not done:
        action, _ = model.predict(obs)
        obs, _, done, _ = env.step(action)

    return action  # 1 = Buy, 2 = Sell, 0 = Hold

# Example Usage:
# df = pd.read_csv("data/historical_data.csv")
# train_rl_agent(df)
# action = predict_trade(df)
# print("Recommended Action:", action)
