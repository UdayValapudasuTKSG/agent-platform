import os
from libs.core.orchestrator import MultiAgentSupervisor

class Agent(MultiAgentSupervisor):
    def __init__(self, project: str, location: str):
        super().__init__(
            project=project,
            location=location,
            agent_names=["researcher", "writer"],
            system_instruction="You are a helpful supervisor agent. You coordinate research and writing tasks. Use the tools provided when asked to research or write summaries."
        )

if __name__ == "__main__":
    project = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    agent = Agent(project=project, location=location)
    
    # Test conversational flow
    print("--- Conversation Start ---")
    print(f"User: Can you research the benefits of meditation and then write a summary?")
    print(f"Agent: {agent.query('Can you research the benefits of meditation and then write a summary?')}")
