import pandas as pd
import pyodbc
import sqlalchemy
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

conn = pyodbc.connect(
    "DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=LLM_KnowledgeBase;Trusted_Connection=yes;"
)

df = pd.read_sql("SELECT Id, Content FROM KnowledgeBase", conn)

documents = df["Content"].tolist()



# from sentence_transformers import SentenceTransformer


model = SentenceTransformer('all-MiniLM-L6-v2')

embeddings = model.encode(documents)

index = faiss.IndexFlatL2(len(embeddings[0]))
index.add(np.array(embeddings))



def search(query, k=3):
    q_embed = model.encode([query])
    _, indices = index.search(np.array(q_embed), k)
    return [documents[i] for i in indices[0]]

results = search("What is SQL used for?")
print(results)



def build_prompt(query, context):
    return f"""
Answer the question using the context below.

Context:
{context}

Question:
{query}
"""

context = "\n".join(results)
prompt = build_prompt("What is SQL used for?", context)

print(prompt)

# ALTER TABLE KnowledgeBase ADD Embedding VARBINARY(MAX);