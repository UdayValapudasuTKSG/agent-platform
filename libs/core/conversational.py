from libs.core.agent import BaseAgent
from vertexai.generative_models import GenerativeModel, ChatSession

class ConversationalAgent(BaseAgent):
    """
    An agent specialized for conversational interaction.
    Manages chat history and session state.
    """
    def __init__(self, project: str, location: str, model_name: str = "gemini-1.5-flash", system_instruction: str = None):
        super().__init__(project, location)
        self.model = GenerativeModel(
            model_name,
            system_instruction=system_instruction
        )
        self.chat = self.model.start_chat()

    def query(self, message: str):
        """
        Send a message to the chat session and return the response.
        """
        response = self.chat.send_message(message)
        return response.text
