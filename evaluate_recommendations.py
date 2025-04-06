import json
from collections import defaultdict

# ------------------------ Load Data ------------------------
with open('data/past_purchases.json', 'r') as f:
    past_purchases = json.load(f)

with open('data/recommendations.json', 'r') as f:
    recommendations = json.load(f)

# Create a lookup for past purchases
user_purchases = defaultdict(set)

# ----------------------- Data Cleanup ----------------------
# Check for any missing or empty 'purchased_product_ids'
for purchase in past_purchases:
    user_id = purchase.get('user_id')  # Safely access user_id
    purchased_product_ids = purchase.get('purchased_product_ids', [])  # Default to empty list if missing
    if not purchased_product_ids:
        print(f"⚠️ User {user_id} has no purchases.")
    else:
        for product_id in purchased_product_ids:
            user_purchases[user_id].add(product_id)

# -------------------- Evaluation Metrics --------------------
def precision_at_k(recommended, relevant, k=10):
    recommended_k = recommended[:k]
    relevant_set = set(relevant)
    hits = sum(1 for item in recommended_k if item in relevant_set)
    return hits / k

def hit_rate(recommended, relevant):
    return int(any(item in relevant for item in recommended))

# --------------------- Evaluation Loop ----------------------
total_users = 0
precision_sum = 0
hit_count = 0

for user in recommendations:
    user_id = user.get('user_id')  # Safely access user_id
    recommended_products = user.get('recommendations', [])

    # Get recommended product IDs
    recommended_ids = [item.get('id') for item in recommended_products if 'id' in item]

    if user_id in user_purchases:
        relevant_ids = user_purchases[user_id]

        # Evaluate Precision@10 and Hit Rate
        prec = precision_at_k(recommended_ids, relevant_ids, k=10)
        hit = hit_rate(recommended_ids, relevant_ids)

        precision_sum += prec
        hit_count += hit
        total_users += 1
    else:
        print(f"⚠️ No past purchases found for user {user_id}, skipping...")

# ------------------------ Results --------------------------
if total_users > 0:
    avg_precision = precision_sum / total_users
    overall_hit_rate = hit_count / total_users

    print("📊 Evaluation Results:")
    print(f"Total Users Evaluated: {total_users}")
    print(f"Average Precision@10: {avg_precision:.4f}")
    print(f"Hit Rate: {overall_hit_rate:.4f}")
else:
    print("⚠️ No users found for evaluation.")
