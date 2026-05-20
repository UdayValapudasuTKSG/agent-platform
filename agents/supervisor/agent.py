from google.adk.agents import Agent

_researcher = Agent(
    name="researcher",
    model="gemini-2.0-flash",
    description="A research agent that provides detailed reports on any topic.",
    instruction=(
        "You are a professional researcher. When given a topic, provide a concise "
        "but detailed research report. Focus on key facts, recent developments, "
        "and important context."
    ),
)

_writer = Agent(
    name="writer",
    model="gemini-2.0-flash",
    description="A writing agent that creates well-structured articles and summaries.",
    instruction=(
        "You are a professional technical writer. When given research data or a topic, "
        "write a well-structured summary or short article using Markdown formatting. "
        "Ensure it is engaging and informative."
    ),
)

root_agent = Agent(
    name="supervisor",
    model="gemini-2.0-flash",
    description="A supervisor agent that coordinates research and writing tasks.",
    instruction=(
        "You are a helpful supervisor agent. You coordinate research and writing tasks. "
        "When asked to research a topic, delegate to the researcher sub-agent. "
        "When asked to write content, delegate to the writer sub-agent. "
        "For combined tasks, first research then write a summary."
    ),
    sub_agents=[_researcher, _writer],
)
