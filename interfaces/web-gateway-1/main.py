import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.cloud import aiplatform
from libs.gcp_utils.config import get_agent_resource_name
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Agent Platform Gateway")


class QueryRequest(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"status": "online", "message": "Agent Platform Gateway is running"}

@app.post("/agents/{agent_name}/query")
async def query_agent(agent_name: str, request: QueryRequest):
    """
    Finds the latest resource ID for the agent and invokes it.
    """
    resource_name = get_agent_resource_name(agent_name)
    if not resource_name:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found or not deployed.")
    
    try:
        # Load the remote Reasoning Engine
        remote_app = aiplatform.ReasoningEngine(resource_name)
        # Invoke the query method
        response = remote_app.query(input_text=request.text)
        return {"agent": agent_name, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
