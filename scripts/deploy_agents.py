import os
import sys
import subprocess
from libs.gcp_utils.config import set_agent_url
from dotenv import load_dotenv

load_dotenv()

_repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)


def _run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    print(f"  $ {' '.join(cmd)}")
    return subprocess.run(cmd, check=True, **kwargs)


def _get_service_url(service_name: str, project: str, region: str) -> str:
    result = _run(
        [
            "gcloud", "run", "services", "describe", service_name,
            f"--project={project}",
            f"--region={region}",
            "--format=value(status.url)",
        ],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def deploy_agent(agent_dir: str):
    agent_name = os.path.basename(agent_dir.rstrip("/\\"))
    service_name = f"agent-{agent_name}"
    project = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
    region = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    print(f"\n--- Deploying Agent: {agent_name} -> Cloud Run service: {service_name} ---")

    _run([
        "adk", "deploy", "cloud_run",
        f"--project={project}",
        f"--region={region}",
        f"--service-name={service_name}",
        "--allow-unauthenticated",
        agent_dir,
    ])

    url = _get_service_url(service_name, project, region)
    set_agent_url(agent_name, url)
    print(f"Deployed {agent_name}: {url}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        for dir_path in sys.argv[1:]:
            deploy_agent(dir_path)
    else:
        agents_root = "agents"
        for folder in sorted(os.listdir(agents_root)):
            path = os.path.join(agents_root, folder)
            if os.path.isdir(path) and os.path.exists(os.path.join(path, "agent.py")):
                deploy_agent(path)
