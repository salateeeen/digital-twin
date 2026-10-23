import gymnasium as gym
from gymnasium import spaces
import numpy as np

class NetworkEnv(gym.Env):
    """
    Custom Network Environment for RL routing agent.
    Updated with a strict reward function to prevent route flapping.
    """
    def __init__(self):
        super().__init__()
        
        # Actions: 0 = NOOP, 1 = HOLD, 2 = REROUTE
        self.action_space = spaces.Discrete(3)
        
        # State: [utilizationPct, latencyMs, packetLossPct]
        self.observation_space = spaces.Box(
            low=np.array([0.0, 0.0, 0.0], dtype=np.float32),
            high=np.array([100.0, 500.0, 100.0], dtype=np.float32),
            dtype=np.float32
        )
        
        self.state = np.array([50.0, 20.0, 0.5], dtype=np.float32)
        self.current_step = 0
        self.max_steps = 100

    def step(self, action):
        self.current_step += 1
        utilization, latency, packet_loss = self.state
        
        if action == 2:  # REROUTE
            if utilization >= 75.0 or latency >= 45.0:
                reward = 10.0  # Huge reward for saving the network
            else:
                reward = -10.0 # Huge penalty for flapping
            
            utilization = max(0.0, utilization - 30.0)
            latency = max(5.0, latency - 15.0)
            packet_loss = max(0.0, packet_loss - 1.0)
            
        elif action == 1:  # HOLD
            reward = -2.0  # Discourage HOLD unless necessary
            utilization += np.random.uniform(-2.0, 5.0)
            
        else:  # NOOP
            if utilization >= 75.0 or latency >= 45.0:
                reward = -10.0  # Huge penalty for ignoring actual congestion
            else:
                reward = 2.0   # Small reward for maintaining peace
                
            utilization += np.random.uniform(-5.0, 10.0)

        self.state = np.array(
            [
                np.clip(utilization, 0.0, 100.0),
                np.clip(latency, 0.0, 500.0),
                np.clip(packet_loss, 0.0, 100.0)
            ], 
            dtype=np.float32
        )
        
        terminated = self.current_step >= self.max_steps
        truncated = False
        
        return self.state, reward, terminated, truncated, {}

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.state = np.array([50.0, 20.0, 0.5], dtype=np.float32)
        self.current_step = 0
        return self.state, {}