import os
import vertexai
from vertexai.generative_models import GenerativeModel
from libs.core.agent import BaseAgent

class Agent(BaseAgent):
    def __init__(self, project: str, location: str):
        super().__init__(project, location)
        self.model = GenerativeModel("gemini-1.5-flash")

    def query(self, topic: str):
        print(f"Researcher: Performing research on {topic}...")
        prompt = f"""
        You are a professional researcher. Provide a concise but detailed research report on the following topic: {topic}.
        Focus on key facts, recent developments, and important context.
        """
        response = self.model.generate_content(prompt)
        return response.text

if __name__ == "__main__":
    project = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project")
    agent = Agent(project=project, location="us-central1")
    print(agent.query("AI Agents"))
