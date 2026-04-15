from openai import OpenAI
import json

client = OpenAI()

# --- TOOL FUNCTIONS ---
def run_sql(query):
    # Replace with real DB execution
    return f"Executed SQL: {query}"

def analyze_data(data):
    return f"Summary: {len(data)} rows processed"

tools = [
    {
        "type": "function",
        "function": {
            "name": "run_sql",
            "description": "Execute SQL query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    }
]

# --- AGENT LOOP ---
def agent(query):
    messages = [{"role": "user", "content": query}]

    while True:
        response = client.chat.completions.create(
            model="gpt-5",
            messages=messages,
            tools=tools
        )

        msg = response.choices[0].message

        if msg.tool_calls:
            for tool_call in msg.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                if name == "run_sql":
                    result = run_sql(args["query"])

                messages.append(msg)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
        else:
            return msg.content

print(agent("Get top 5 customers by revenue"))