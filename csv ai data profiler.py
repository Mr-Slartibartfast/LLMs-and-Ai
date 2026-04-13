import pandas as pd
from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY")

def profile_dataset(df):
    summary = {
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "null_counts": df.isnull().sum().to_dict(),
        "sample": df.head(5).to_dict()
    }

    prompt = f"""
    You are a data engineer. Analyze this dataset summary and describe:
    - What the dataset represents
    - Data quality issues
    - Suggested transformations
    - Potential business use cases
    
    {summary}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


df = pd.read_csv("data.csv")
print(profile_dataset(df))