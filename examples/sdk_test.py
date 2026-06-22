from avimind import AviMind

client = AviMind("http://localhost:8000")

print(client.health())

memory = client.remember(
    user_id="avinash",
    agent_id="sdk-agent",
    session_id="sdk-test-001",
    memory_type="project_memory",
    content="User is testing the AviMind Python SDK.",
    tags=["sdk", "python", "test"],
    importance=0.9,
)

print(memory)

results = client.search(
    user_id="avinash",
    query="What SDK is the user testing?",
)

print(results)

context = client.context(
    user_id="avinash",
    query="What SDK is the user testing?",
)

print(context)