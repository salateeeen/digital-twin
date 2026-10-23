import numpy as np
from stable_baselines3 import PPO
from environment import NetworkEnv

def test_model():
    print("Loading the trained PPO agent...")
    model_path = "models/ppo_network_agent"
    
    try:
        model = PPO.load(model_path)
    except FileNotFoundError:
        print(f"Error: Model not found at {model_path}. Please train the agent first.")
        return

    env = NetworkEnv()
    obs, info = env.reset()
    
    print("\n--- Starting Inference Test ---")
    print(f"Initial State: Util={obs[0]:.1f}%, Latency={obs[1]:.1f}ms, Loss={obs[2]:.1f}%")
    
    action_map = {0: "NOOP", 1: "HOLD", 2: "REROUTE"}
    
    for step in range(10):
        # deterministic=True forces the agent to pick the best learned action
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        
        action_name = action_map.get(int(action), "UNKNOWN")
        
        print(f"\nStep {step + 1}: Agent Action -> {action_name}")
        print(f"New State  : Util={obs[0]:.1f}%, Latency={obs[1]:.1f}ms, Loss={obs[2]:.1f}%")
        print(f"Reward     : {reward}")
        
        if terminated or truncated:
            print("\nSimulation finished.")
            break

if __name__ == "__main__":
    test_model()