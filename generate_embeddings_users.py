import json
import requests
import numpy as np
from pathlib import Path

# Constants
OLLAMA_EMBEDDING_URL = "http://localhost:11434/api/embeddings"
MODEL_NAME = "nomic-embed-text"
EMBEDDING_SIZE = 768

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

def main():
    with open("data/users.json", "r") as f:
        users = json.load(f)

    embedded_users = []

    for user in users:
        print(f"🔄 Embedding interests for: {user['name']}")
        interest_text = ", ".join(user["interests"])
        vector = get_embedding(interest_text)
        if vector is not None:
            user["embedding"] = vector.tolist()
            embedded_users.append(user)

    with open("data/users_with_embeddings.json", "w") as f:
        json.dump(embedded_users, f, indent=2)

    print("✅ User embeddings saved to data/users_with_embeddings.json")

if __name__ == "__main__":
    main()
