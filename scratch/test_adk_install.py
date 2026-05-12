import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    install("google-adk")
    print("Successfully installed google-adk")
    import google.adk.agents as agents
    print("ADK Agents available:", dir(agents))
except Exception as e:
    print(f"Failed to install/import google-adk: {e}")
