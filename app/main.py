from agent import run_agent

print("Currency LLM Agent Started")
print("Type 'exit' to quit\n")

while True:

    query = input("You: ")

    if query.lower() == "exit":
        break

    response = run_agent(query)

    print("Agent:", response)