from google.adk.agents import Agent

root_agent = Agent(
    name="support_agent",
    model="gemini-2.0-flash",
    description="A specialized conversational support agent.",
    instruction="You are a specialized conversational agent. Help the user with their requests.",
)
