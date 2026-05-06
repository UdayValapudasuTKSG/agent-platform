import os
from google.cloud import secretmanager
from google.api_core import exceptions

def get_secret(secret_id, project_id=None):
    """Retrieves a secret value from GCP Secret Manager."""
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    
    try:
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except exceptions.NotFound:
        return None

def set_secret(secret_id, value, project_id=None):
    """Sets/Updates a secret value in GCP Secret Manager."""
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{project_id}"
    
    # Check if secret exists
    secret_name = f"projects/{project_id}/secrets/{secret_id}"
    try:
        client.get_secret(request={"name": secret_name})
    except exceptions.NotFound:
        # Create secret if it doesn't exist
        client.create_secret(
            request={
                "parent": parent,
                "secret_id": secret_id,
                "secret": {"replication": {"automatic": {}}},
            }
        )
    
    # Add a new version
    client.add_secret_version(
        request={"parent": secret_name, "payload": {"data": value.encode("UTF-8")}}
    )

def get_agent_resource_name(agent_name):
    """Helper to get the reasoning engine resource name for a given agent."""
    secret_id = f"agent-id-{agent_name.replace('_', '-')}"
    return get_secret(secret_id)

def set_agent_resource_name(agent_name, resource_name):
    """Helper to store the reasoning engine resource name for a given agent."""
    secret_id = f"agent-id-{agent_name.replace('_', '-')}"
    set_secret(secret_id, resource_name)
