import pandas as pd
from openai import OpenAI

client = OpenAI()

# Load dataset
df = pd.read_csv("data.csv")

def summarize_data(df):
    summary = {
        "columns": list(df.columns),
        "shape": df.shape,
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "sample": df.head(5).to_dict()
    }
    return summary

def ask_llm(summary, question):
    prompt = f"""
    You are a data analyst.

    Dataset Summary:
    {summary}

    User Question:
    {question}

    Analyze the dataset and give insights.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# Run it
summary = summarize_data(df)
result = ask_llm(summary, "What trends or issues do you see?")

print(result)