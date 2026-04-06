from openai import OpenAI
client = OpenAI()

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                },
                "required": ["city"]
            }
        }
    }
]

def get_weather(city):
    return f"The weather in {city} is sunny."

def run_agent(user_input):
    response = client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "user", "content": user_input}],
        tools=tools
    )

    msg = response.choices[0].message

    if msg.tool_calls:
        tool_call = msg.tool_calls[0]
        result = get_weather(**tool_call.function.arguments)

        return client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "user", "content": user_input},
                msg,
                {"role": "tool", "content": result}
            ]
        ).choices[0].message.content

    return msg.content