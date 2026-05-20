import sys
import subprocess
from dotenv import load_dotenv

load_dotenv()

USAGE = """
Usage:
  python scripts/local_run.py gateway               # Start the FastAPI gateway
  python scripts/local_run.py run   <agent-name>    # CLI chat with an agent (adk run)
  python scripts/local_run.py web   <agent-name>    # Browser UI for an agent (adk web)
  python scripts/local_run.py api   <agent-name>    # Local REST API server (adk api_server)
"""


def main():
    if len(sys.argv) < 2:
        print(USAGE)
        return

    command = sys.argv[1]

    if command == "gateway":
        print("Starting Gateway locally...")
        subprocess.run(["python", "interfaces/web-gateway-1/main.py"])

    elif command in ("run", "web", "api"):
        agent_name = sys.argv[2] if len(sys.argv) > 2 else "test-adk-agent"
        agent_path = f"agents/{agent_name}"
        adk_command = "api_server" if command == "api" else command
        print(f"Starting '{agent_name}' with: adk {adk_command} {agent_path}")
        subprocess.run(["adk", adk_command, agent_path])

    else:
        print(USAGE)


if __name__ == "__main__":
    main()
