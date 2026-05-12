from libs.core.adk_agent import ADKAgent

class Agent(ADKAgent):
    def __init__(self, project: str, location: str):
        super().__init__(
            project=project,
            location=location,
            name="adk_conversational_agent",

            description="A helpful assistant built with Google ADK.",
            instruction="You are a helpful assistant. Use your tools to help the user if available.",
            model="gemini-1.5-flash",
            tools=[] # Add your Python functions here
        )

if __name__ == "__main__":
    import os
    agent = Agent(
        project=os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project"),
        location=os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    )
    print(agent.query("Hello! Who are you?"))
