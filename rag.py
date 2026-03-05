from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")


def build_vector_db(pages):

    texts = [p["text"] for p in pages]

    embeddings = model.encode(texts)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings))

    return index, texts


def search(query, vector_db, texts):

    query_embedding = model.encode([query])

    D, I = vector_db.search(query_embedding, 3)

    results = [texts[i] for i in I[0]]

    return results