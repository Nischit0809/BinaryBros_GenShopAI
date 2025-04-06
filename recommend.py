import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load data
with open("data/products_with_embeddings.json", "r") as f:
    products = json.load(f)

with open("data/users_with_embeddings.json", "r") as f:
    users = json.load(f)

with open("data/past_purchases.json", "r") as f:
    past_purchases_data = json.load(f)

# Build lookup structures
product_dict = {product["id"]: product for product in products}
user_dict = {user["user_id"]: user for user in users}
user_purchases_map = {u["user_id"]: set(u["purchased_product_ids"]) for u in past_purchases_data}


def recommend_products(user_id, top_n=3, category_boost=0.1):
    user = user_dict.get(user_id)
    if not user:
        print(f"User {user_id} not found.")
        return []

    user_vector = np.array(user["embedding"])
    preferred_categories = user.get("preferred_categories", [])
    past_purchases = user_purchases_map.get(user_id, set())

    scored_products = []

    for product in products:
        if product["id"] in past_purchases:
            continue

        product_vector = np.array(product["embedding"])
        similarity = cosine_similarity([user_vector], [product_vector])[0][0]
        explanation_parts = []

        if similarity > 0.45:
            explanation_parts.append("🧠 Matches your interests")
        if product["category"] in preferred_categories:
            similarity += category_boost
            explanation_parts.append("📂 From your preferred categories")
        past_similarities = [
            cosine_similarity([product_vector], [np.array(product_dict[pid]["embedding"])])[0][0]
            for pid in past_purchases if pid in product_dict
        ]
        if past_similarities and max(past_similarities) > 0.45:
            explanation_parts.append("🛍️ Similar to things you've bought")

        explanation = " & ".join(explanation_parts) or "Matched your profile"
        scored_products.append((product, similarity, explanation))

    scored_products.sort(key=lambda x: x[1], reverse=True)

    print(f"\n✨ Top {top_n} Recommendations for {user['name']} (User ID: {user_id}):\n")
    for i, (product, score, explanation) in enumerate(scored_products[:top_n], start=1):
        print(f"{i}. 🛍️ {product['name']} ({product['category']})")
        print(f"   ➤ {product['description']}")
        print(f"   💰 ${product['price']}  |  🔗 Similarity Score: {score:.4f}")
        print(f"   📌 Why: {explanation}\n")

    return [p[0]["id"] for p in scored_products[:top_n]]


def simulate_purchase(user_id, product_id):
    user_data = next((u for u in past_purchases_data if u["user_id"] == user_id), None)
    product = product_dict.get(product_id)

    if not user_data:
        print(f"User {user_id} not found in past purchases.")
        return
    if not product:
        print(f"Product {product_id} not found.")
        return

    if product_id not in user_data["purchased_product_ids"]:
        user_data["purchased_product_ids"].append(product_id)
        print(f"✅ Purchased: {product['name']}")
    else:
        print(f"⚠️ Already purchased: {product['name']}")

    # Save changes
    with open("data/past_purchases.json", "w") as f:
        json.dump(past_purchases_data, f, indent=2)


def show_purchase_history(user_id):
    purchases = user_purchases_map.get(user_id, set())
    if not purchases:
        print("🗃️ No past purchases.")
        return

    print("\n📦 Purchase History:")
    for pid in purchases:
        product = product_dict.get(pid)
        if product:
            print(f"✔️ {product['name']} (${product['price']}) - {product['category']}")


def cli_loop():
    print("🛍️ Welcome to the CLI Recommender!")
    user_id = int(input("Enter your User ID: "))
    if user_id not in user_dict:
        print("❌ Invalid User ID.")
        return

    while True:
        print("\n📋 Menu:")
        print("1. Show recommendations")
        print("2. Buy a recommended product")
        print("3. Show purchase history")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            global last_recommended_ids
            last_recommended_ids = recommend_products(user_id)
        elif choice == "2":
            if not last_recommended_ids:
                print("⚠️ Please view recommendations first.")
                continue
            try:
                pick = int(input(f"Select product number (1-{len(last_recommended_ids)}): ")) - 1
                if 0 <= pick < len(last_recommended_ids):
                    simulate_purchase(user_id, last_recommended_ids[pick])
                    # Refresh map
                    user_purchases_map[user_id].add(last_recommended_ids[pick])
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Invalid input.")
        elif choice == "3":
            show_purchase_history(user_id)
        elif choice == "4":
            print("👋 Exiting. See you!")
            break
        else:
            print("❌ Invalid option.")


if __name__ == "__main__":
    last_recommended_ids = []
    cli_loop()
