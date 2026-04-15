from openai import OpenAI
import pyodbc
import numpy as np

client = OpenAI()

# --- DB CONNECTION ---
conn = pyodbc.connect(
    "DRIVER={SQL Server};SERVER=localhost;DATABASE=KnowledgeBase;Trusted_Connection=yes;"
)
cursor = conn.cursor()

# --- EMBEDDING FUNCTION ---
def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=text
    )
    return response.data[0].embedding

# --- STORE DOCUMENTS ---
def store_document(doc_id, text):
    embedding = get_embedding(text)
    vector_str = ",".join(map(str, embedding))

    cursor.execute("""
        INSERT INTO Documents (doc_id, content, embedding)
        VALUES (?, ?, ?)
    """, doc_id, text, vector_str)
    conn.commit()

# --- COSINE SIMILARITY ---
def cosine_similarity(vec1, vec2):
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# --- RETRIEVE TOP MATCHES ---
def search(query, top_k=3):
    query_vec = get_embedding(query)

    cursor.execute("SELECT doc_id, content, embedding FROM Documents")
    results = []

    for doc_id, content, emb_str in cursor.fetchall():
        emb = list(map(float, emb_str.split(",")))
        score = cosine_similarity(query_vec, emb)
        results.append((score, content))

    results.sort(reverse=True)
    return [r[1] for r in results[:top_k]]

# --- GENERATE ANSWER ---
def ask(query):
    context = "\n".join(search(query))

    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": "Answer using provided context only."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
        ]
    )

    return response.choices[0].message.content

print(ask("What does our customer churn dataset say?"))