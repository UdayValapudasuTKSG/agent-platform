from libs.core.orchestrator import MultiAgentSupervisor

class Agent(MultiAgentSupervisor):
    def __init__(self, project: str, location: str):
        super().__init__(
            project=project,
            location=location,
            agent_names=["researcher", "writer"], # List sub-agents here
            system_instruction="You are a supervisor coordinating multiple agents."
        )

if __name__ == "__main__":
    import os
    agent = Agent(
        project=os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project"),
        location=os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    )
    print(agent.query("Please research AI trends and summarize them."))
