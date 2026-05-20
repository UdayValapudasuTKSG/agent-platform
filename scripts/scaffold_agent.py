import os
import shutil
import argparse
import json
from datetime import datetime, timezone

DEFAULT_TEMPLATES_HUB = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "agent_templates")
)

ADK_PYPROJECT = """\
[project]
name = "{name}"
version = "0.1.0"
dependencies = [
    "google-adk>=1.0.0",
    "google-cloud-aiplatform[reasoningengine]>=1.50.0",
    "cloudpickle>=3.0.0",
]

[tool.setuptools]
packages = ["tools"]
"""


def scaffold_agent(name: str, agent_type: str, hub_path: str | None = None):
    if hub_path is None:
        hub_path = DEFAULT_TEMPLATES_HUB

    registry_path = os.path.join(hub_path, "registry.json")
    if not os.path.exists(registry_path):
        print(f"Error: Template Hub not found at {hub_path}")
        return

    with open(registry_path) as f:
        registry = json.load(f)

    template_info = next(
        (t for t in registry["templates"] if t["id"] == agent_type), None
    )
    if not template_info:
        available = [t["id"] for t in registry["templates"]]
        print(f"Error: Template type '{agent_type}' not found. Available: {', '.join(available)}")
        return

    template_dir = os.path.join(hub_path, template_info["path"])
    target_dir = f"agents/{name}"

    if os.path.exists(target_dir):
        print(f"Error: Agent directory '{target_dir}' already exists.")
        return
    if not os.path.exists(template_dir):
        print(f"Error: Template directory '{template_dir}' not found.")
        return

    print(f"Scaffolding {template_info['name']} (v{template_info['version']}) -> {name}...")
    shutil.copytree(template_dir, target_dir)

    with open(os.path.join(target_dir, "template_info.json"), "w") as f:
        json.dump(
            {
                "template_id": template_info["id"],
                "template_version": template_info["version"],
                "scaffolded_at": datetime.now(timezone.utc).isoformat(),
            },
            f,
            indent=2,
        )

    pyproject_path = os.path.join(target_dir, "pyproject.toml")
    with open(pyproject_path, "w") as f:
        f.write(ADK_PYPROJECT.format(name=name))

    print(f"Successfully created agent at {target_dir}")
    print(f"Next steps:")
    print(f"  1. Edit {target_dir}/agent.py to customize your agent")
    print(f"  2. Run locally:  python scripts/local_run.py web {name}")
    print(f"  3. Deploy:       python scripts/deploy_agents.py {target_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scaffold a new ADK agent.")
    parser.add_argument("--name", required=True, help="Name of the agent")
    parser.add_argument("--type", required=True, help="Template type (from registry)")
    parser.add_argument("--hub", help="Path to the Agent Templates Hub")
    args = parser.parse_args()
    scaffold_agent(args.name, args.type, args.hub)
