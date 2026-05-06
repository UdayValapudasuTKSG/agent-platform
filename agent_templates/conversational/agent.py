from libs.core.conversational import ConversationalAgent

class Agent(ConversationalAgent):
    def __init__(self, project: str, location: str):
        super().__init__(
            project=project,
            location=location,
            system_instruction="You are a specialized conversational agent. Help the user with their requests."
        )

if __name__ == "__main__":
    import os
    agent = Agent(
        project=os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project"),
        location=os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    )
    print(agent.query("Hello!"))
