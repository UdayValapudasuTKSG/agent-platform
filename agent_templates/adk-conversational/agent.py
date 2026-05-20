from google.adk.agents import Agent

root_agent = Agent(
    name="my_agent",
    model="gemini-2.0-flash",
    description="A helpful conversational agent.",
    instruction="You are a helpful assistant. Answer the user's questions clearly and concisely.",
)
