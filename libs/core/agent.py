import vertexai
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """
    Abstract base class for all agents in the framework.
    Provides standardized initialization and interface.
    """
    def __init__(self, project: str, location: str):
        self.project = project
        self.location = location
        vertexai.init(project=project, location=location)

    @abstractmethod
    def query(self, *args, **kwargs):
        """
        The main entry point for the agent.
        Must be implemented by subclasses.
        """
        pass
