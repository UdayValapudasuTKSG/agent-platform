import os
import sys
import shutil
import argparse

def scaffold_agent(name, agent_type):
    target_dir = f"agents/{name}"
    template_dir = f"agent_templates/{agent_type}"
    
    if os.path.exists(target_dir):
        print(f"Error: Agent directory '{target_dir}' already exists.")
        return

    if not os.path.exists(template_dir):
        print(f"Error: Template '{agent_type}' not found.")
        return

    print(f"Scaffolding {agent_type} agent: {name}...")
    shutil.copytree(template_dir, target_dir)
    
    # Create a basic pyproject.toml if missing
    pyproject_path = os.path.join(target_dir, "pyproject.toml")
    if not os.path.isfile(pyproject_path):
        with open(pyproject_path, "w") as f:
            f.write(f"""[project]
name = "{name}"
version = "0.1.0"
dependencies = [
    "google-cloud-aiplatform[reasoningengine,langchain]>=1.50.0",
    "cloudpickle==3.0.0",
]

[tool.setuptools]
packages = ["tools"]
""")

    print(f"Successfully created agent at {target_dir}")
    print(f"Next steps: Edit {target_dir}/agent.py to customize your logic.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scaffold a new agent.")
    parser.add_argument("--name", required=True, help="Name of the agent")
    parser.add_argument("--type", choices=["conversational", "multi-agent"], default="conversational", help="Type of agent")
    
    args = parser.parse_args()
    scaffold_agent(args.name, args.type)
