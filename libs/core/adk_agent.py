import os
import inspect
from google.adk.agents import Agent
from vertexai.preview.reasoning_engines.templates.adk import AdkApp
from libs.core.agent import BaseAgent
from libs.core.utils import load_agent_config
from typing import List, Callable, Optional

class ADKAgent(BaseAgent):
    """
    An agent built using the modern Google Agent Development Kit (ADK).
    Automatically loads prompt.txt and config.json if they exist in the agent directory.
    """
    def __init__(
        self, 
        project: str, 
        location: str, 
        name: str,
        tools: Optional[List[Callable]] = None
    ):
        super().__init__(project, location)
        
        # 1. Determine the directory of the actual agent implementation
        agent_dir = os.path.dirname(inspect.getfile(self.__class__))
        
        # 2. Load Config with defaults
        config = load_agent_config(agent_dir, {
            "model": "gemini-1.5-flash",
            "description": "A helpful assistant built with Google ADK.",
            "system_instruction": "You are a helpful assistant. Use your tools to help the user if available."
        })
        
        # 3. Initialize the ADK Agent
        self.agent = Agent(
            name=name,
            description=config["description"],
            instruction=config["system_instruction"],
            model=config["model"],
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



