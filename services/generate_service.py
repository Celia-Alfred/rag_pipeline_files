import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(query, retrieved_documents):
    context = "\n\n".join(retrieved_documents)

    prompt = f"""
You are a helpful company policy assistant.

Answer the user's question using only the information provided in the context.

If the answer is not available in the context, say:
"I don't have enough information in the company policies to answer that."

Context:
{context}

User question:
{query}

Answer:
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content