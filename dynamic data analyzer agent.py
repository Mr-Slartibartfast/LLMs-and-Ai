import pandas as pd
import traceback
from openai import OpenAI

client = OpenAI()

df = pd.read_csv("data.csv")

def run_code(code):
    try:
        local_vars = {"df": df}
        exec(code, {}, local_vars)
        return local_vars.get("result", "No result returned")
    except Exception as e:
        return str(e)

def agent(question):
    system_prompt = """
    You are a data analyst.

    You can write Python code using pandas.
    The dataset is loaded as a DataFrame called `df`.

    Rules:
    - Always store final answer in variable `result`
    - Only write Python code
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    )

    code = response.choices[0].message.content

    print("Generated Code:\n", code)

    output = run_code(code)

    return output

# Example
print(agent("What is the average sales by region?"))