import json

def simulate_purchase(user_id, product_id):
    with open("data/past_purchases.json", "r") as f:
        past_purchases = json.load(f)

    for user in past_purchases:
        if user["user_id"] == user_id:
            if product_id not in user["purchased_product_ids"]:
                user["purchased_product_ids"].append(product_id)
                print(f"✅ User {user_id} purchased product {product_id}")
            else:
                print(f"⚠️ Product {product_id} already purchased by user {user_id}")

    with open("data/past_purchases.json", "w") as f:
        json.dump(past_purchases, f, indent=2)

# Example Usage:
simulate_purchase(user_id=2, product_id=12)
