from google.adk.agents import Agent
import vertexai

vertexai.init(project="test-project", location="us-central1")

a = Agent(
    name="test_agent",
    description="test",
    instruction="test",
    model="gemini-1.5-flash"
)

try:
    print("Testing run_live...")
    # run_live is likely the method
    # It might return an iterable or a response object
    res = a.run_live("Hello")
    print("Response type:", type(res))
    print("Response:", res)
except Exception as e:
    print("run_live failed:", e)

try:
    print("Testing __call__...")
    res = a("Hello")
    print("Call response:", res)
except Exception as e:
    print("__call__ failed:", e)
