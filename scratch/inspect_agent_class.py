from google.adk.agents import Agent
print("Agent members:", [m for m in dir(Agent) if not m.startswith("_")])
# Also inspect an instance if possible
try:
    a = Agent(name="test", description="test", instruction="test", model="gemini-1.5-flash")
    print("Agent instance members:", [m for m in dir(a) if not m.startswith("_")])
except Exception as e:
    print("Could not instantiate Agent:", e)
