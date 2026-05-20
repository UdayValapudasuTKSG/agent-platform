import os
from dotenv import load_dotenv

load_dotenv()


def get_config_value(key, default=None):
    return os.environ.get(key, default)


def get_agent_url(agent_name: str) -> str | None:
    """Get the Cloud Run service URL for an agent."""
    project = os.environ.get("GOOGLE_CLOUD_PROJECT")

    if project:
        try:
            from google.cloud import secretmanager
            client = secretmanager.SecretManagerServiceClient()
            name = f"projects/{project}/secrets/agent-url-{agent_name}/versions/latest"
            response = client.access_secret_version(request={"name": name})
            return response.payload.data.decode("UTF-8")
        except Exception:
            pass

    env_key = f"AGENT_URL_{agent_name.upper().replace('-', '_')}"
    return os.environ.get(env_key)


def set_agent_url(agent_name: str, url: str):
    """Store the Cloud Run service URL after a successful deploy."""
    env_key = f"AGENT_URL_{agent_name.upper().replace('-', '_')}"
    os.environ[env_key] = url

    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if project:
        try:
            from google.cloud import secretmanager
            client = secretmanager.SecretManagerServiceClient()
            secret_id = f"agent-url-{agent_name}"
            parent = f"projects/{project}"

            try:
                client.create_secret(
                    request={
                        "parent": parent,
                        "secret_id": secret_id,
                        "secret": {"replication": {"automatic": {}}},
                    }
                )
            except Exception:
                pass

            client.add_secret_version(
                request={
                    "parent": f"{parent}/secrets/{secret_id}",
                    "payload": {"data": url.encode("UTF-8")},
                }
            )
            print(f"URL stored in Secret Manager: {secret_id}")
            return
        except Exception as e:
            print(f"Warning: Secret Manager write failed ({e}). Falling back to .env")

    env_file = ".env"
    lines = []
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            lines = f.readlines()

    found = False
    for i, line in enumerate(lines):
        if line.startswith(f"{env_key}="):
            lines[i] = f"{env_key}={url}\n"
            found = True
            break
    if not found:
        lines.append(f"{env_key}={url}\n")

    with open(env_file, "w") as f:
        f.writelines(lines)
    print(f"URL stored in .env: {env_key}")


def get_agent_resource_name(agent_name: str):
    """Get the Reasoning Engine resource name for an agent.

    Checks Secret Manager first (CI / Cloud Run). Falls back to env var
    so local dev works without Secret Manager access.
    """
    project = os.environ.get("GOOGLE_CLOUD_PROJECT")

    if project:
        try:
            from google.cloud import secretmanager
            client = secretmanager.SecretManagerServiceClient()
            name = f"projects/{project}/secrets/agent-id-{agent_name}/versions/latest"
            response = client.access_secret_version(request={"name": name})
            return response.payload.data.decode("UTF-8")
        except Exception:
            pass

    # Local dev fallback — read from env var (populated by .env or a prior deploy)
    env_key = f"AGENT_ID_{agent_name.upper().replace('-', '_')}"
    return os.environ.get(env_key)


def set_agent_resource_name(agent_name: str, resource_name: str):
    """Store the Reasoning Engine resource name after a successful deploy.

    In CI / GCP environments: writes to Secret Manager so the Cloud Run
    gateway can read it at runtime.
    In local dev: falls back to writing the .env file.
    Always updates the current process environment so immediate callers work.
    """
    env_key = f"AGENT_ID_{agent_name.upper().replace('-', '_')}"
    os.environ[env_key] = resource_name

    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if project:
        try:
            from google.cloud import secretmanager
            client = secretmanager.SecretManagerServiceClient()
            secret_id = f"agent-id-{agent_name}"
            parent = f"projects/{project}"

            # Create the secret if it doesn't exist yet
            try:
                client.create_secret(
                    request={
                        "parent": parent,
                        "secret_id": secret_id,
                        "secret": {"replication": {"automatic": {}}},
                    }
                )
            except Exception:
                pass  # Already exists

            client.add_secret_version(
                request={
                    "parent": f"{parent}/secrets/{secret_id}",
                    "payload": {"data": resource_name.encode("UTF-8")},
                }
            )
            print(f"Resource name stored in Secret Manager: {secret_id}")
            return
        except Exception as e:
            print(f"Warning: Secret Manager write failed ({e}). Falling back to .env")

    # Local dev fallback — write to .env file
    env_file = ".env"
    lines = []
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            lines = f.readlines()

    found = False
    for i, line in enumerate(lines):
        if line.startswith(f"{env_key}="):
            lines[i] = f"{env_key}={resource_name}\n"
            found = True
            break
    if not found:
        lines.append(f"{env_key}={resource_name}\n")

    with open(env_file, "w") as f:
        f.writelines(lines)
    print(f"Resource name stored in .env: {env_key}")
