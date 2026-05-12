from google.adk.agents import Agent
from vertexai.preview.reasoning_engines.templates.adk import AdkApp
import vertexai

vertexai.init(project="test-project", location="us-central1")

a = Agent(
    name="test_agent",
    description="test",
    instruction="test",
    model="gemini-1.5-flash"
)
app = AdkApp(agent=a)

print("Testing app.stream_query...")
try:
    for event in app.stream_query(input_text="Hello"):
        print(f"Event: {event}")
except Exception as e:
    print("stream_query failed:", e)
