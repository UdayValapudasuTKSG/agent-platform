from google.adk.agents import Agent

root_agent = Agent(
    name="healthcare_supervisor",
    model="gemini-2.0-flash",
    description="A healthcare supervisor agent that helps users with healthcare-related requests.",
    instruction=(
        "You are a helpful healthcare supervisor agent. You assist users with "
        "healthcare-related questions and coordinate with specialized agents as needed. "
        "Always recommend consulting a qualified medical professional for specific medical advice."
    ),
)
