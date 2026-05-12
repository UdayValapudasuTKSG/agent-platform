import os
import sys
import tomllib
import vertexai
from vertexai.preview import reasoning_engines
from vertexai.preview.reasoning_engines.templates import adk
from libs.gcp_utils.config import set_agent_resource_name
from dotenv import load_dotenv

# Load environment variables
load_dotenv()



def deploy_agent(agent_dir):
    agent_name = os.path.basename(agent_dir)
    print(f"--- Deploying Agent: {agent_name} ---")
    
    # 1. Parse pyproject.toml for requirements
    pyproject_path = os.path.join(agent_dir, "pyproject.toml")
    with open(pyproject_path, "rb") as f:
        config = tomllib.load(f)
    
    requirements = config.get("project", {}).get("dependencies", [])
    print(f"Requirements: {requirements}")
    
    # 2. Import the Agent class dynamically
    # Add agent_dir to sys.path
    sys.path.append(agent_dir)
    from agent import Agent
    
    # 3. Initialize Vertex AI
    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    staging_bucket = os.environ.get("STAGING_BUCKET")
    
    vertexai.init(project=project, location=location, staging_bucket=staging_bucket)
    
    # 4. Deploy to Reasoning Engine
    print("Creating Reasoning Engine instance...")
    
    agent_instance = Agent(project=project, location=location)
    
    # If the agent uses the ADK, wrap it in an AdkApp
    if hasattr(agent_instance, "agent") and "google.adk" in str(type(agent_instance.agent)):
        print("Detected ADK Agent. Wrapping in AdkApp...")
        deployable_obj = adk.AdkApp(agent=agent_instance.agent)
    else:
        deployable_obj = agent_instance

    remote_app = reasoning_engines.ReasoningEngine.create(
        deployable_obj,
        requirements=requirements,
        display_name=f"agent-{agent_name}",
    )

    
    resource_name = remote_app.resource_name
    print(f"Successfully deployed: {resource_name}")
    
    # 5. Store ID
    set_agent_resource_name(agent_name, resource_name)
    print(f"Resource name stored in .env file.")


if __name__ == "__main__":
    # In CI, we would pass changed directories
    if len(sys.argv) > 1:
        for dir_path in sys.argv[1:]:
            deploy_agent(dir_path)
    else:
        # Default: deploy all agents in agents/
        agents_root = "agents"
        for folder in os.listdir(agents_root):
            path = os.path.join(agents_root, folder)
            if os.path.isdir(path):
                deploy_agent(path)
