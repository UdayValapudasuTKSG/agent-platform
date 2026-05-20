import os
import shutil

TEMPLATE_PYPROJECT = "agent_templates/adk-conversational/pyproject.toml"


def sync_templates():
    agents_root = "agents"
    if not os.path.exists(TEMPLATE_PYPROJECT):
        print(f"Template not found: {TEMPLATE_PYPROJECT}")
        return

    for folder in os.listdir(agents_root):
        target_dir = os.path.join(agents_root, folder)
        if not os.path.isdir(target_dir):
            continue
        dst = os.path.join(target_dir, "pyproject.toml")
        shutil.copy2(TEMPLATE_PYPROJECT, dst)
        print(f"  Synced pyproject.toml -> {folder}")


if __name__ == "__main__":
    sync_templates()
