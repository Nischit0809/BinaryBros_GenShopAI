import json
import numpy as np
from pathlib import Path

# === Load User Embeddings === #
with open("data/users_with_embeddings.json", "r") as f:
    users = json.load(f)

# === Load Product Embeddings === #
with open("data/products_with_embeddings.json", "r") as f:
    products = json.load(f)

# === Similarity Function === #
def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1, dtype=np.float32)
    vec2 = np.array(vec2, dtype=np.float32)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# === Recommendation Function === #
def recommend_products_for_user(user, top_k=3):
    user_embedding = user["embedding"]
    scored_products = []

    for product in products:
        similarity = cosine_similarity(user_embedding, product["embedding"])
        scored_products.append((product, similarity))

    scored_products.sort(key=lambda x: x[1], reverse=True)
    return scored_products[:top_k]

# === Run Recommendations === #
for user in users:
    print(f"\n👤 Recommendations for: {user['name']} (Interests: {user['interests']})\n")
    top_products = recommend_products_for_user(user)

    for product, score in top_products:
        print(f"🛒 {product['name']} ({product['category']})")
        print(f"    ➤ {product['description']}")
        print(f"    💰 ${product['price']}  |  🔗 Similarity: {score:.4f}\n")
