import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from libs.gcp_utils.config import get_agent_url
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Agent Platform Gateway")


def _auth_headers(audience: str) -> dict:
    """Return a Bearer ID-token header when running on GCP; empty dict locally."""
    try:
        import google.auth.transport.requests
        import google.oauth2.id_token
        req = google.auth.transport.requests.Request()
        token = google.oauth2.id_token.fetch_id_token(req, audience)
        return {"Authorization": f"Bearer {token}"}
    except Exception:
        return {}


class QueryRequest(BaseModel):
    text: str
    user_id: str = "default_user"
    session_id: str = "default_session"


@app.get("/")
def read_root():
    return {"status": "online", "message": "Agent Platform Gateway is running"}


@app.post("/agents/{agent_name}/query")
async def query_agent(agent_name: str, request: QueryRequest):
    url = get_agent_url(agent_name)
    if not url:
        raise HTTPException(
            status_code=404,
            detail=f"Agent '{agent_name}' not found or not deployed.",
        )

    payload = {
        "app_name": agent_name,
        "user_id": request.user_id,
        "session_id": request.session_id,
        "new_message": {
            "role": "user",
            "parts": [{"text": request.text}],
        },
    }

    try:
        async with httpx.AsyncClient(timeout=120) as client:
            resp = await client.post(
                f"{url}/run",
                json=payload,
                headers=_auth_headers(url),
            )
            resp.raise_for_status()
            events = resp.json()

        # Extract the last text part from the agent's response events
        text_parts = [
            part.get("text", "")
            for event in events
            for part in event.get("content", {}).get("parts", [])
            if part.get("text")
        ]
        response_text = text_parts[-1] if text_parts else ""
        return {"agent": agent_name, "response": response_text}

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
