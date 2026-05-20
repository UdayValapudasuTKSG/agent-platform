from google.adk import Agent

# Define your agent
agent = Agent(
    name="multi_tool_agent",
    description="A multi-tool agent for demonstration purposes."
)

@agent.tool
def get_weather(city: str) -> str:
    """Returns the weather for a given city."""
    return f"The weather in {city} is sunny."

@agent.action
def chat(message: str) -> str:
    """Standard chat interface."""
    return f"You said: {message}. I am a multi-tool agent."
