#pip install transformers torch

from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")

result = generator("Explain data engineering in simple terms:", max_length=100)

print(result[0]["generated_text"])