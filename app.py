from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime
from firebase_config import db  # Firestore client
from db.database import init_db, save_chat_memory, fetch_user_chats  # SQLite functions

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# ------------------- Initialize SQLite -------------------
init_db()

# ------------------- Load Data -------------------

PRODUCTS_PATH = os.path.join('data', 'products_with_embeddings.json')
RECOMMENDATIONS_PATH = os.path.join('data', 'recommendations.json')

try:
    with open(PRODUCTS_PATH, 'r') as f:
        all_products = json.load(f)
except Exception as e:
    print(f"❌ Error loading products file: {e}")
    all_products = []

try:
    with open(RECOMMENDATIONS_PATH, 'r') as f:
        recommendations_data = json.load(f)
except Exception as e:
    print(f"❌ Error loading recommendations file: {e}")
    recommendations_data = []

# ------------------- Routes -------------------

# 🛍 Get all products
@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify(all_products), 200

# 💳 Handle checkout and log to Firestore
@app.route('/api/checkout', methods=['POST'])
def checkout():
    try:
        data = request.get_json()
        user_id = data.get("userId")
        cart = data.get("cart", [])

        if not user_id or not cart:
            return jsonify({"error": "userId and cart are required"}), 400

        total = sum(item.get("price", 0) for item in cart)
        log_data = {
            "userId": user_id,
            "cart": cart,
            "total": total,
            "timestamp": datetime.utcnow()
        }

        db.collection("checkouts").add(log_data)

        return jsonify({"message": "Checkout successful and logged"}), 200

    except Exception as e:
        print(f"❌ Checkout error: {e}")
        return jsonify({"error": str(e)}), 500

# 🧠 Get personalized recommendations
@app.route('/api/recommendations/<user_id>', methods=['GET'])
def get_recommendations(user_id):
    try:
        user_id = int(user_id)  # ✅ Convert to int for comparison

        # ✅ Check local recommendations.json
        user_recommendations = next(
            (user for user in recommendations_data if user['user_id'] == user_id),
            None
        )

        if user_recommendations:
            return jsonify({
                "message": "✅ Recommendations fetched from recommendations.json",
                "recommendations": user_recommendations['recommendations']
            }), 200

        # 🔄 Fallback to Firestore-based logic
        checkouts_ref = db.collection('checkouts').where('userId', '==', user_id)
        docs = checkouts_ref.stream()

        purchased_ids = set()
        category_counts = {}

        for doc in docs:
            data = doc.to_dict()
            for item in data.get('cart', []):
                item_id = item.get('id')
                category = item.get('category')
                if item_id:
                    purchased_ids.add(item_id)
                if category:
                    category_counts[category] = category_counts.get(category, 0) + 1

        if not category_counts:
            return jsonify({
                "message": "⚠️ No purchase history found. Cannot generate personalized recommendations.",
                "recommendations": []
            }), 200

        # 🎯 Recommend products from most purchased categories
        top_categories = sorted(category_counts, key=category_counts.get, reverse=True)[:2]
        recommendations = [
            p for p in all_products
            if p.get('category') in top_categories and p.get('id') not in purchased_ids
        ][:10]

        return jsonify({
            "message": "✅ Recommendations fetched from Firestore.",
            "recommendations": recommendations
        }), 200

    except Exception as e:
        print(f"❌ Recommendation error: {e}")
        return jsonify({"error": str(e)}), 500

# 💬 Save chat message and response to SQLite
@app.route('/api/chat', methods=['POST'])
def save_chat():
    try:
        data = request.get_json()
        user_id = data.get("userId")
        message = data.get("message")
        response = data.get("response")

        if not user_id or not message or not response:
            return jsonify({"error": "userId, message, and response are required"}), 400

        save_chat_memory(user_id, message, response)

        return jsonify({"message": "Chat saved successfully"}), 200

    except Exception as e:
        print(f"❌ Chat save error: {e}")
        return jsonify({"error": str(e)}), 500

# 📜 Fetch chat history for a user
@app.route('/api/chat/<user_id>', methods=['GET'])
def get_chat_history(user_id):
    try:
        user_id = int(user_id)
        chats = fetch_user_chats(user_id)
        chat_list = [
            {"message": msg, "response": res, "timestamp": ts}
            for msg, res, ts in chats
        ]
        return jsonify({"chat_history": chat_list}), 200

    except Exception as e:
        print(f"❌ Fetch chat error: {e}")
        return jsonify({"error": str(e)}), 500

# ------------------- Start Server -------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)
