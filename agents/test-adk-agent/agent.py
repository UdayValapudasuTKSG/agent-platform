from google.adk.agents import Agent

root_agent = Agent(
    name="adk_conversational_agent",
    model="gemini-2.0-flash",
    description="A helpful assistant built with Google ADK.",
    instruction="You are a helpful assistant. Use your tools to help the user if available.",
)
