import ollama


def generate_answer(question, context_chunks):

    context = "\n".join(context_chunks)

    prompt = f"""
You are a helpful study assistant.

Use ONLY the notes below to answer the question.

NOTES:
{context}

QUESTION:
{question}

Rules:
- Do NOT use outside knowledge
- If the answer is not in the notes say:
"I don't have enough information."
"""

    response = ollama.chat(
        model="phi:latest",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]