import vertexai
from libs.core.agent import BaseAgent
from vertexai.generative_models import GenerativeModel, Tool, FunctionDeclaration
from vertexai.preview import reasoning_engines
from libs.gcp_utils.config import get_agent_resource_name

class MultiAgentSupervisor(BaseAgent):
    """
    Base class for supervisors that coordinate multiple sub-agents.
    Handles sub-agent discovery and tool registration.
    """
    def __init__(self, project: str, location: str, agent_names: list[str], system_instruction: str = None):
        super().__init__(project, location)
        self.sub_agents = {}
        self.tool_declarations = []

        for name in agent_names:
            agent_id = get_agent_resource_name(name)
            if agent_id:
                # Connected to remote reasoning engine
                self.sub_agents[name] = reasoning_engines.ReasoningEngine(agent_id)
            else:
                # Placeholder for local fallback logic
                self.sub_agents[name] = None
            
            # Register as a tool
            self.tool_declarations.append(
                FunctionDeclaration(
                    name=f"call_{name}",
                    description=f"Invokes the {name} agent to perform its specialized task.",
                    parameters={
                        "type": "object",
                        "properties": {
                            "input_text": {"type": "string", "description": "The input for the agent"}
                        },
                        "required": ["input_text"]
                    },
                )
            )

        self.tools = Tool(function_declarations=self.tool_declarations)
        self.model = GenerativeModel(
            "gemini-1.5-flash",
            tools=[self.tools],
            system_instruction=system_instruction
        )
        self.chat = self.model.start_chat()

    def query(self, message: str):
        response = self.chat.send_message(message)
        
        while response.candidates[0].function_calls:
            for function_call in response.candidates[0].function_calls:
                name = function_call.name.replace("call_", "")
                args = function_call.args
                
                if name in self.sub_agents and self.sub_agents[name]:
                    result = self.sub_agents[name].query(topic=args.get("input_text", ""))
                else:
                    result = f"Error: Agent {name} not found or not connected."

                response = self.chat.send_message(
                    vertexai.generative_models.Part.from_function_response(
                        name=function_call.name,
                        response={"content": result}
                    )
                )
        return response.text
