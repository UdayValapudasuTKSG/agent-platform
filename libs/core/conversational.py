from libs.core.agent import BaseAgent
from vertexai.generative_models import GenerativeModel, ChatSession

class ConversationalAgent(BaseAgent):
    """
    An agent specialized for conversational interaction.
    Manages chat history and session state.
    """
    def __init__(self, project: str, location: str):
        super().__init__(project, location)
        
        # Determine the directory of the actual agent implementation
        import os, inspect
        agent_dir = os.path.dirname(inspect.getfile(self.__class__))
        
        # Load Config with defaults
        from libs.core.utils import load_agent_config
        config = load_agent_config(agent_dir, {
            "model": "gemini-1.5-flash",
            "system_instruction": "You are a specialized conversational agent. Help the user with their requests."
        })
        
        self.model = GenerativeModel(
            config["model"],
            system_instruction=config["system_instruction"]
        )
        self.chat = self.model.start_chat()


    def query(self, message: str):
        """
        Send a message to the chat session and return the response.
        """
        response = self.chat.send_message(message)
        return response.text
