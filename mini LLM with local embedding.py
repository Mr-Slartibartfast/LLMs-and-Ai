import pyodbc
import numpy as np
from sentence_transformers import SentenceTransformer

# -------------------------------
# DB CONNECTION
# -------------------------------
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=LLM_KnowledgeBase;"
    "Trusted_Connection=yes;"
)
cursor = conn.cursor()

# -------------------------------
# LOAD LOCAL EMBEDDING MODEL
# -------------------------------
model = SentenceTransformer('all-MiniLM-L6-v2')

# -------------------------------
# SAMPLE DATA (replace with your own)
# -------------------------------
documents = [
    "SQL is used to query databases",
    "Python is great for data engineering",
    "Large language models can generate text",
    "Embeddings convert text into vectors",
    "Machine learning enables AI systems"
]

# -------------------------------
# INSERT + EMBED DATA
# -------------------------------
for doc in documents:
    embedding = model.encode(doc)

    # Convert to binary for SQL storage
    embedding_bytes = np.array(embedding).astype(np.float32).tobytes()
    
    # Insert document first
cursor.execute("""
    INSERT INTO Documents (content)
    OUTPUT INSERTED.id
    VALUES (?)
""", doc)

doc_id = cursor.fetchone()[0]

# Insert embedding
cursor.execute("""
    INSERT INTO Embeddings (document_id, embedding)
    VALUES (?, ?)
""", doc_id, embedding_bytes)

conn.commit()

print("✅ Documents inserted with embeddings")

# -------------------------------
# SEARCH FUNCTION
# -------------------------------
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search(query, top_k=3):
    query_embedding = model.encode(query)

    cursor.execute("""
        SELECT d.content, e.embedding
        FROM Documents d
        JOIN Embeddings e ON d.id = e.document_id
    """)
    results = []

    for content, emb in cursor.fetchall():
        emb_array = np.frombuffer(emb, dtype=np.float32)

        score = cosine_similarity(query_embedding, emb_array)
        results.append((content, score))

    # Sort by similarity
    results.sort(key=lambda x: x[1], reverse=True)

    return results[:top_k]

# -------------------------------
# TEST QUERY
# -------------------------------
query = "How do I work with databases?"
results = search(query)

print("\n🔍 Query:", query)
print("\nTop Results:\n")

for content, score in results:
    print(f"Score: {score:.4f} | {content}")