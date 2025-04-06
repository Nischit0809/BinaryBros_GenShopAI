import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load products with embeddings
with open("data/products_with_embeddings.json", "r") as f:
    products = json.load(f)

# Load users with embeddings
with open("data/users_with_embeddings.json", "r") as f:
    users = json.load(f)

# Configuration
TOP_N = 3
CATEGORY_BOOST = 0.1

all_recommendations = []

for user in users:
    user_vector = np.array(user["embedding"])
    preferred_categories = user.get("preferred_categories", [])
    past_purchases = set(user.get("past_purchases", []))

    scored = []

    for product in products:
        if product["id"] in past_purchases:
            continue

        product_vector = np.array(product["embedding"])
        similarity = cosine_similarity([user_vector], [product_vector])[0][0]

        # Boost for preferred categories
        boosted = similarity
        explanation = f"Similarity score: {similarity:.4f}"

        if product["category"] in preferred_categories:
            boosted += CATEGORY_BOOST
            explanation += f" + Category boost ({CATEGORY_BOOST})"

        scored.append({
            "product_id": product["id"],
            "name": product["name"],
            "category": product["category"],
            "description": product["description"],
            "price": product["price"],
            "score": round(boosted, 4),
            "explanation": explanation
        })

    # Sort & take top N
    top_recommendations = sorted(scored, key=lambda x: x["score"], reverse=True)[:TOP_N]

    all_recommendations.append({
        "user_id": user["user_id"],
        "name": user["name"],
        "recommendations": top_recommendations
    })

# Save to JSON
with open("data/recommendations.json", "w") as f:
    json.dump(all_recommendations, f, indent=2)

print("✅ Batch recommendations saved to data/recommendations.json")
