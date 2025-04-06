import json
import requests
import numpy as np

OLLAMA_EMBEDDING_URL = "http://localhost:11434/api/embeddings"
MODEL_NAME = "nomic-embed-text"

def get_embedding(text, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.post(OLLAMA_EMBEDDING_URL, json={
                "model": MODEL_NAME,
                "prompt": text
            })
            data = response.json()
            embedding = data.get("embedding", [])

            if isinstance(embedding, list) and len(embedding) == 768:
                return np.array(embedding, dtype=np.float32)
            else:
                print(f"⚠️ Attempt {attempt + 1}: Invalid embedding length ({len(embedding)}). Retrying...")

        except Exception as e:
            print(f"❌ Exception on attempt {attempt + 1}: {e}")

    print("❌ Failed to get a valid 768-length embedding after retries.")
    return None

def main():
    with open("data/products.json", "r") as f:
        products = json.load(f)

    embedded_products = []

    for product in products:
        print(f"🔄 Embedding: {product['name']}")
        description = product["description"]
        vector = get_embedding(description)
        if vector is not None:
            product["embedding"] = vector.tolist()
            embedded_products.append(product)

    with open("data/products_with_embeddings.json", "w") as f:
        json.dump(embedded_products, f, indent=2)

    print("✅ Embeddings saved to data/products_with_embeddings.json")

if __name__ == "__main__":
    main()
