import sys
import subprocess
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def run_local(target):
    if target == "gateway":
        print("Starting Gateway locally...")
        subprocess.run(["python", "interfaces/web-gateway-1/main.py"], env=os.environ)
    elif target == "agent":
        agent_name = sys.argv[2] if len(sys.argv) > 2 else "healthcare-supervisor"
        print(f"Testing Agent '{agent_name}' locally...")
        subprocess.run(["python", f"agents/{agent_name}/agent.py"], env=os.environ)
    else:
        print("Usage: python scripts/local_run.py [gateway|agent <name>]")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_local(sys.argv[1])
    else:
        print("Usage: python scripts/local_run.py [gateway|agent <name>]")
