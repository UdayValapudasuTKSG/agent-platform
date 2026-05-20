from google.adk.agents import Agent, SequentialAgent

_step_one = Agent(
    name="step_one",
    model="gemini-2.0-flash",
    description="First step: analyzes input and extracts key points.",
    instruction="Analyze the following input and extract the key points clearly and concisely.",
)

_step_two = Agent(
    name="step_two",
    model="gemini-2.0-flash",
    description="Second step: generates a structured response from the key points.",
    instruction="Based on the key points provided, generate a well-structured and informative response.",
)

root_agent = SequentialAgent(
    name="prompt_chaining_agent",
    description="A prompt-chaining agent that runs steps in sequence, feeding each output into the next.",
    sub_agents=[_step_one, _step_two],
)
