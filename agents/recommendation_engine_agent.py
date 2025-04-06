import json
import numpy as np
from pathlib import Path

# Set up paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"

USERS_FILE = DATA_DIR / "users_with_embeddings.json"
PRODUCTS_FILE = DATA_DIR / "products_with_embeddings.json"
RECOMMENDATIONS_FILE = DATA_DIR / "recommendations.json"

TOP_K = 5  # number of top recommendations per user

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def recommend_products():
    print("🤖 Running Recommendation Engine...")

    users = load_json(USERS_FILE)
    products = load_json(PRODUCTS_FILE)

    all_recommendations = []

    for user in users:
        user_id = user["user_id"]
        user_vector = user["embedding"]

        # Compute similarity with all products
        scored_products = []
        for product in products:
            product_vector = product["embedding"]
            score = cosine_similarity(user_vector, product_vector)
            scored_products.append((product, score))

        # Sort by score (descending) and take top K
        top_products = sorted(scored_products, key=lambda x: x[1], reverse=True)[:TOP_K]

        # Prepare output
        recommendations = [p[0] for p in top_products]
        all_recommendations.append({
            "user_id": user_id,
            "name": user["name"],
            "recommendations": recommendations
        })

    # Save to file
    with open(RECOMMENDATIONS_FILE, "w") as f:
        json.dump(all_recommendations, f, indent=2)

    print(f"✅ Saved top {TOP_K} recommendations for {len(users)} users to recommendations.json")

if __name__ == "__main__":
    recommend_products()
