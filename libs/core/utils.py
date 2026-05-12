import os
import json

def load_agent_config(agent_dir: str, default_config: dict):
    """
    Helper to load prompt.txt and config.json from an agent directory.
    """
    config = default_config.copy()
    
    # Load from config.json
    config_path = os.path.join(agent_dir, "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config.update(json.load(f))
    
    # Load from prompt.txt
    prompt_path = os.path.join(agent_dir, "prompt.txt")
    if os.path.exists(prompt_path):
        with open(prompt_path, "r") as f:
            config["system_instruction"] = f.read().strip()
            
    return config
