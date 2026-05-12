from google.adk.agents import Agent
from vertexai.preview.reasoning_engines.templates.adk import AdkApp
from libs.core.agent import BaseAgent
from typing import List, Callable, Optional

class ADKAgent(BaseAgent):
    """
    An agent built using the modern Google Agent Development Kit (ADK).
    """
    def __init__(
        self, 
        project: str, 
        location: str, 
        name: str,
        description: str,
        instruction: str,
        model: str = "gemini-1.5-flash",
        tools: Optional[List[Callable]] = None
    ):
        super().__init__(project, location)
        self.agent = Agent(
            name=name,
            description=description,
            instruction=instruction,
            model=model,
            tools=tools or []
        )
        self.app = AdkApp(agent=self.agent)

    def query(self, message: str, user_id: str = "default_user"):
        """
        Runs the ADK agent via AdkApp and returns the concatenated text response.
        """
        full_text = ""
        for event in self.app.stream_query(message=message, user_id=user_id):
            if hasattr(event, "text"):
                full_text += event.text
            elif isinstance(event, str):
                full_text += event
        return full_text

