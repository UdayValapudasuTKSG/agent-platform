from google.adk.agents import Agent
import vertexai
import asyncio

vertexai.init(project="test-project", location="us-central1")

a = Agent(
    name="test_agent",
    description="test",
    instruction="test",
    model="gemini-1.5-flash"
)

async def test():
    print("Starting run_live...")
    async for event in a.run_live("Hello"):
        print(f"Event type: {type(event)}")
        print(f"Event: {event}")

if __name__ == "__main__":
    asyncio.run(test())
