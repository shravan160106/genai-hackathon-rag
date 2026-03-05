import ollama

def generate_answer(question, context_chunks):

    if len(context_chunks) == 0:
        return "I don't have information."

    context = "\n".join(context_chunks)

    prompt = f"""
You are a helpful assistant.

Answer ONLY using the notes below.

Notes:
{context}

Question:
{question}

If the answer is not in the notes say:
"I don't have information."
"""

    response = ollama.chat(
        model="phi",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]