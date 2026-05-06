import vertexai
from vertexai.preview import reasoning_engines

class Agent:
    """
    Base Agent Template.
    The Reasoning Engine hosts this class and invokes its methods.
    """
    def __init__(self, project: str, location: str):
        self.project = project
        self.location = location
        vertexai.init(project=project, location=location)

    def query(self, input_text: str):
        """
        Main entry point for the agent.
        """
        # Implement your logic here
        return f"Agent Response to: {input_text}"

if __name__ == "__main__":
    # Local testing
    agent = Agent(project="your-project", location="us-central1")
    print(agent.query("Hello!"))
