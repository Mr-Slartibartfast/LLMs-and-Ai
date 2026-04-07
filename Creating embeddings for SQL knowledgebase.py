from openai import OpenAI
import pyodbc
import numpy as np
import struct

client = OpenAI(api_key="API-key")

def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding



def save_embedding_to_sql(content, embedding):
    conn = pyodbc.connect(
        "DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=LLM_KnowledgeBase;Trusted_Connection=yes;"
    )
    cursor = conn.cursor()

    # Convert list → binary
    binary_embedding = struct.pack(f"{len(embedding)}f", *embedding)

    cursor.execute("""
        INSERT INTO dbo.KnowledgeBase (Title, Content, Embedding)
        VALUES (?, ?, ?)
    """, ("Auto Entry", content, binary_embedding))

    conn.commit()
    conn.close()

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search_knowledge_base(query):
    query_embedding = get_embedding(query)

    conn = pyodbc.connect(
        "DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=YourDB;Trusted_Connection=yes;"
    )
    cursor = conn.cursor()

    cursor.execute("SELECT Content, Embedding FROM KnowledgeBase")

    best_match = None
    best_score = -1

    for row in cursor.fetchall():
        content = row[0]
        embedding_binary = row[1]

        embedding = list(struct.unpack(f"{len(embedding_binary)//4}f", embedding_binary))

        score = cosine_similarity(query_embedding, embedding)

        if score > best_score:
            best_score = score
            best_match = content

    conn.close()
    return best_match