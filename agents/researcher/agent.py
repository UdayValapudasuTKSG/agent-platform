from google.adk.agents import Agent

root_agent = Agent(
    name="researcher",
    model="gemini-2.0-flash",
    description="A research agent that provides detailed reports on any topic.",
    instruction=(
        "You are a professional researcher. When given a topic, provide a concise "
        "but detailed research report. Focus on key facts, recent developments, "
        "and important context."
    ),
)
