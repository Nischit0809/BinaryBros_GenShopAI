import json
import numpy as np
from collections import defaultdict
from pathlib import Path

# Dynamically resolve correct data directory relative to this script
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"

# Paths to data files
BEHAVIOR_LOG = DATA_DIR / "behavior_log.json"
USERS_FILE = DATA_DIR / "users_with_embeddings.json"
PRODUCTS_FILE = DATA_DIR / "products_with_embeddings.json"

# Weight for blending old + new embedding
BLEND_WEIGHT = 0.6  # 60% old, 40% from new behavior

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def update_user_profiles():
    if not BEHAVIOR_LOG.exists():
        print("❌ No behavior log found. Nothing to update.")
        return

    print("🔁 Updating user profiles based on behavior log...")

    behaviors = load_json(BEHAVIOR_LOG)
    users = load_json(USERS_FILE)
    products = load_json(PRODUCTS_FILE)

    # Ensure all keys are strings for matching
    user_dict = {str(user["user_id"]): user for user in users}
    product_dict = {str(product["id"]): product for product in products}

    # Debug print to confirm loaded IDs
    print("👥 Available user IDs:", list(user_dict.keys()))
    print("📦 Available product IDs:", list(product_dict.keys()))

    # Map user → list of product embeddings
    user_behavior_vectors = defaultdict(list)

    for entry in behaviors:
        uid = str(entry["user_id"])
        pid = str(entry["product_id"])

        if uid in user_dict and pid in product_dict:
            embedding = product_dict[pid]["embedding"]
            user_behavior_vectors[uid].append(embedding)

    updated_count = 0

    for uid, vectors in user_behavior_vectors.items():
        user = user_dict[uid]
        old_vector = np.array(user["embedding"])
        new_vector = np.mean(np.array(vectors), axis=0)

        # Blend old and new (to preserve history)
        blended_vector = (BLEND_WEIGHT * old_vector) + ((1 - BLEND_WEIGHT) * new_vector)
        user["embedding"] = blended_vector.tolist()
        updated_count += 1

    # Save updated users
    save_json(USERS_FILE, list(user_dict.values()))
    print(f"✅ Updated embeddings for {updated_count} users.")

    # Clear the behavior log
    BEHAVIOR_LOG.write_text("[]")
    print("🧹 Cleared behavior log.\n")

if __name__ == "__main__":
    update_user_profiles()
