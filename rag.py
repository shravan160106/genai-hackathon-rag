from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def chunk_text(text, chunk_size=120, overlap=30):

    words = text.split()
    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size
        chunk = " ".join(words[start:end])

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def build_vector_db(pages):

    texts = []

    for p in pages:
        texts.extend(chunk_text(p["text"]))

    embeddings = model.encode(texts)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings))

    return index, texts


def search(query, vector_db, texts, top_k=2):

    query_embedding = model.encode([query])

    D, I = vector_db.search(query_embedding, top_k)

    results = [texts[i] for i in I[0]]

    return results