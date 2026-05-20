from google.adk.agents import Agent

root_agent = Agent(
    name="writer",
    model="gemini-2.0-flash",
    description="A writing agent that creates well-structured articles and summaries.",
    instruction=(
        "You are a professional technical writer. When given research data or a topic, "
        "write a well-structured summary or short article using Markdown formatting. "
        "Ensure it is engaging and informative."
    ),
)
