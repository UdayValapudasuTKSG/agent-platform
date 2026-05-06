import os
import shutil

def sync_templates():
    template_path = "agent_templates/prompt-chaining"
    agents_root = "agents"
    
    # Files to sync (excluding those likely modified by developers like agent.py if they already exist)
    # For now, let's just sync the structure but skip agent.py if it exists
    files_to_sync = ["pyproject.toml"] 
    
    for folder in os.listdir(agents_root):
        target_dir = os.path.join(agents_root, folder)
        if os.path.isdir(target_dir):
            print(f"Syncing {folder}...")
            for f in files_to_sync:
                src = os.path.join(template_path, f)
                dst = os.path.join(target_dir, f)
                if os.path.exists(src):
                    shutil.copy2(src, dst)
                    print(f"  Updated {f}")

if __name__ == "__main__":
    sync_templates()
