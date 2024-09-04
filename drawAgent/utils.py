from langchain_core.messages import AIMessage, HumanMessage

# Define a custom pretty printer
def pretty_print(result):
    if "agent" in result:
        for message in result["agent"]["messages"]:
            if isinstance(message, AIMessage):
                print(f"AI: {message.content}")
            elif isinstance(message, HumanMessage):
                print(f"Human: {message.content}")
            elif "additional_kwargs" in message:
                tool_calls = message["additional_kwargs"].get("tool_calls", [])
                for call in tool_calls:
                    if call["type"] == "function":
                        print(
                            f"Tool Call: {call['function']['name']} with args {call['function']['arguments']}"
                        )
    if "tools" in result:
        for message in result["tools"]["messages"]:
            print(f"Tool ({message.name}): {message.content}")
