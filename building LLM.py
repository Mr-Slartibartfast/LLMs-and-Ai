#pip install sentence-transformers faiss-cpu openai

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

documents = [
    "Python is used for data engineering",
    "SQL is used for querying databases",
    "ETL pipelines move data"
]

embeddings = model.encode(documents)

index = faiss.IndexFlatL2(len(embeddings[0]))
index.add(np.array(embeddings))

def search(query):
    q_embed = model.encode([query])
    _, idx = index.search(np.array(q_embed), k=2)
    return [documents[i] for i in idx[0]]

print(search("What is SQL used for?"))