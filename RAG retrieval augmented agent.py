import pyodbc
from openai import OpenAI

client = OpenAI()

def query_knowledge_base(question):
    conn = pyodbc.connect(
        "DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=KnowledgeBase;Trusted_Connection=yes;"
    )
    cursor = conn.cursor()

    cursor.execute("""
        SELECT TOP 3 content
        FROM documents
        ORDER BY similarity_score DESC
    """)

    return "\n".join(row[0] for row in cursor.fetchall())

def rag_agent(question):
    context = query_knowledge_base(question)

    prompt = f"""
    Use the context below to answer the question.

    Context:
    {context}

    Question:
    {question}
    """

    response = client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content