import os
import vertexai
from vertexai.generative_models import GenerativeModel
from libs.core.agent import BaseAgent

class Agent(BaseAgent):
    def __init__(self, project: str, location: str):
        super().__init__(project, location)
        self.model = GenerativeModel("gemini-1.5-flash")

    def query(self, research_data: str):
        print("Writer: Generating a structured summary...")
        prompt = f"""
        You are a professional technical writer. Based on the following research data, write a well-structured summary or short article.
        Use Markdown formatting. Ensure it is engaging and informative.

        Research Data:
        {research_data}
        """
        response = self.model.generate_content(prompt)
        return response.text

if __name__ == "__main__":
    project = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project")
    agent = Agent(project=project, location="us-central1")
    print(agent.query("Some facts about AI Agents include they are autonomous and use LLMs."))
