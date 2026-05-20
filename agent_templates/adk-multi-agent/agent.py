from google.adk.agents import Agent

_sub_agent_one = Agent(
    name="sub_agent_one",
    model="gemini-2.0-flash",
    description="Handles task A.",
    instruction="You handle task A. Be concise and thorough.",
)

_sub_agent_two = Agent(
    name="sub_agent_two",
    model="gemini-2.0-flash",
    description="Handles task B.",
    instruction="You handle task B. Be concise and thorough.",
)

root_agent = Agent(
    name="supervisor",
    model="gemini-2.0-flash",
    description="A supervisor that delegates tasks to specialized sub-agents.",
    instruction=(
        "You are a supervisor agent. Delegate tasks to your sub-agents based on the user's request. "
        "Use sub_agent_one for task A and sub_agent_two for task B."
    ),
    sub_agents=[_sub_agent_one, _sub_agent_two],
)
