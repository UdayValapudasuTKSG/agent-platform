import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_config_value(key, default=None):
    """Retrieves a configuration value from environment variables."""
    return os.environ.get(key, default)

def get_agent_resource_name(agent_name):
    """Helper to get the reasoning engine resource name for a given agent."""
    # Try AGENT_ID_AGENT_NAME (uppercase, underscores)
    env_key = f"AGENT_ID_{agent_name.upper().replace('-', '_')}"
    return get_config_value(env_key)

def set_agent_resource_name(agent_name, resource_name):
    """
    Helper to store the reasoning engine resource name.
    In local .env mode, we append/update the .env file.
    """
    env_key = f"AGENT_ID_{agent_name.upper().replace('-', '_')}"
    env_file = ".env"
    
    # Read existing lines
    lines = []
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            lines = f.readlines()
    
    # Update or add the key
    found = False
    for i, line in enumerate(lines):
        if line.startswith(f"{env_key}="):
            lines[i] = f"{env_key}={resource_name}\n"
            found = True
            break
    
    if not found:
        lines.append(f"{env_key}={resource_name}\n")
    
    # Write back to .env
    with open(env_file, "w") as f:
        f.writelines(lines)
    
    # Also update current session
    os.environ[env_key] = resource_name

