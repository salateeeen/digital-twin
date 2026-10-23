from pathlib import Path
from stable_baselines3 import PPO
from environment import NetworkEnv

def train_model():
    print("Initializing Network Environment...")
    env = NetworkEnv()

    print("Initializing PPO Agent...")
    model = PPO("MlpPolicy", env, verbose=1)
    
    print("Starting training process (10,000 timesteps)...")
    model.learn(total_timesteps=50000)
    
    # Create models directory if it doesn't exist
    models_dir = Path("models")
    models_dir.mkdir(parents=True, exist_ok=True)
    model_path = models_dir / "ppo_network_agent"
    
    print("Saving the trained model...")
    model.save(str(model_path))
    print(f"Model saved successfully at: {model_path}.zip")

if __name__ == "__main__":
    train_model()