# GCP Agent Engine Deployment Guide

This guide outlines the standard procedures for deploying and updating agents to GCP Agent Engine using the Google Agent Development Kit (ADK).

## Getting Started

### 1. Authentication
Login to Google Cloud and set the application default credentials:
```bash
gcloud auth login
gcloud auth application-default login
```

### 2. Project Setup
Set your project ID:
```bash
PROJECT_ID=prj-d-apm0001234-01 # REPLACE WITH YOUR PROJECT ID
gcloud config set project $PROJECT_ID
export CLOUDSDK_CORE_PROJECT=$PROJECT_ID
```

*(Optional) Test access to project:*
```bash
gcloud storage buckets list --format="json(name)"
```

## Agent Development

### Install ADK
```bash
pip install google-adk
```

### Build a Multi-tool Agent
1. Create the agent structure:
   ```bash
   mkdir multi_tool_agent/
   echo "from . import agent" > multi_tool_agent/__init__.py
   touch multi_tool_agent/agent.py
   touch multi_tool_agent/.env
   ```
2. Configure the model and logic in `agent.py`.
3. Start the CLI or Web UI for testing:
   ```bash
   adk run multi_tool_agent
   adk web --port 8000
   ```

## Deployment

### Standard Deployment
Deploy your agent directly from the CLI:
```bash
PROJECT_ID=prj-d-apm0001234-01
LOCATION_ID=us-central1

adk deploy agent_engine \
  --project=$PROJECT_ID \
  --region=$LOCATION_ID \
  --display_name="My First Agent" \
  multi_tool_agent
```

### Pipeline Deployment
This project includes a `.gitlab-ci.yml` template that automates deployment. 
- **Stages**: `auth` -> `deploy` -> `update`
- **Environment Variables**: Configure `PROJECT_ID`, `LOCATION_ID`, and `SERVICE_ACCOUNT` in the GitLab CI/CD settings or in the YAML file.

## Testing the Reasoning Engine
After deployment, you can test your agent using `curl`:
```bash
TOKEN=$(gcloud auth print-access-token)
curl -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     https://$LOCATION_ID-aiplatform.googleapis.com/v1/projects/$PROJECT_ID/locations/$LOCATION_ID/reasoningEngines/$RESOURCE_ID \
     -d '{"class_method": "async_create_session", "input": {"user_id": "u_123"}}'
```

## (Optional) Gemini Enterprise Agent Registration
To register your agent with Gemini Enterprise:
```bash
curl -X POST -H "Authorization: Bearer $(gcloud auth print-access-token)" \
     -H "Content-Type: application/json" \
     -H "X-Goog-User-Project: ${PROJECT_ID}" \
     "https://${ENDPOINT_LOCATION}-discoveryengine.googleapis.com/v1alpha/projects/${PROJECT_ID}/locations/${ENDPOINT_LOCATION}/collections/default_collection/engines/${APP_ID}/assistants/default_assistant/agents" \
     -d '{
       "displayName": "${DISPLAY_NAME}",
       "description": "${DESCRIPTION}",
       "adk_agent_definition": {
         "provisioned_reasoning_engine": {
           "reasoning_engine":"projects/${PROJECT_ID}/locations/${REASONING_ENGINE_LOCATION}/reasoningEngines/${ADK_RESOURCE_ID}"
         }
       }
     }'
```
