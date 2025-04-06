import json
import numpy as np
import requests

# === Constants === #
EMBEDDING_SIZE = 768  # Match generate_embeddings.py
OLLAMA_EMBEDDING_URL = "http://localhost:11434/api/embeddings"
MODEL_NAME = "nomic-embed-text"

# === Embedding Function === #
def get_embedding(text, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.post(OLLAMA_EMBEDDING_URL, json={
                "model": MODEL_NAME,
                "prompt": text
            })
            data = response.json()
            embedding = data.get("embedding", [])

            if isinstance(embedding, list) and len(embedding) == EMBEDDING_SIZE:
                return np.array(embedding, dtype=np.float32)
            else:
                print(f"⚠️ Attempt {attempt + 1}: Invalid embedding length ({len(embedding)}). Retrying...")

        except Exception as e:
            print(f"❌ Exception on attempt {attempt + 1}: {e}")

    print("❌ Failed to get a valid embedding after retries.")
    return None

# === Similarity Calculation === #
def cosine_similarity(vec1, vec2):
    dot = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot / (norm1 * norm2)

# === Semantic Search === #
def semantic_search(query, top_k=3):
    # Load product embeddings
    with open("data/products_with_embeddings.json", "r") as f:
        products = json.load(f)

    # Embed the search query
    query_embedding = get_embedding(query)
    if query_embedding is None:
        print("❌ Failed to get embedding for query.")
        return []

    # Calculate similarity for each product
    results = []
    for product in products:
        prod_embedding = np.array(product["embedding"], dtype=np.float32)
        similarity = cosine_similarity(query_embedding, prod_embedding)
        results.append((product, similarity))

    # Sort results by similarity
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_k]

# === Run the Search === #
if __name__ == "__main__":
    query = input("🔎 Enter your search query: ")
    top_results = semantic_search(query)

    print("\n✨ Top Matching Products:\n")
    for product, score in top_results:
        print(f"🛍️ {product['name']} ({product['category']})")
        print(f"   ➤ {product['description']}")
        print(f"   💰 ${product['price']}  |  🔗 Similarity Score: {score:.4f}")
        print()
