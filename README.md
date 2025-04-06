# 🛒 Personalized E-commerce Recommendation System (Backend)

This project implements a multi-agent backend for personalized e-commerce recommendations using user behavior, embeddings, and memory. Built with Python and Flask.

---

## 📁 Project Structure

```
ecommerce-reco-agents/
│
├── app.py                          # Main backend server
├── generate_embeddings.py         # Product embeddings with Ollama
├── generate_embeddings_users.py   # User embeddings with Ollama
│
├── data/                          # JSON data files
│   ├── products.json
│   ├── products_with_embeddings.json
│   ├── users.json
│   ├── users_with_embeddings.json
│   ├── recommendations.json
│   └── ...
│
├── db/
│   ├── database.py                # SQLite logic
│   ├── ecommerce.db              # SQLite DB file
│   └── init_db.sql               # DB schema
│
├── requirements.txt
└── README.md
```

---

## 🔧 Setup Instructions

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Install SQLite Extension (Optional)

To explore the database easily:

- Install "SQLite Viewer" or "SQLite Explorer" extension in VS Code.
- Open `ecommerce.db` from the `db/` folder.

---

## 🤖 Embeddings with Ollama

### Install Ollama (if not already)

- Visit [https://ollama.com](https://ollama.com) and install for your OS.
- Start the Ollama server:
  ```bash
  ollama serve
  ```

### Pull the embedding model

```bash
ollama pull nomic-embed-text
```

### Run product embeddings

```bash
python generate_embeddings.py
```

### Run user embeddings

```bash
python generate_embeddings_users.py
```

---

## 🚀 Running the API Server

```bash
python app.py
```

By default, the API runs on `http://localhost:5000`.

---

## 🧪 API Testing Guide

You can test endpoints using tools like **curl**, **Thunder Client**, or **Postman**.

### 1. ✅ Get all products

```bash
curl http://localhost:5000/api/products
```

### 2. 💳 Simulate a Checkout

```bash
curl -X POST http://localhost:5000/api/checkout \
  -H "Content-Type: application/json" \
  -d '{
    "userId": 1,
    "cart": [{"id": "P123", "name": "Product A", "price": 99, "category": "Fashion"}]
}'
```

### 3. 🎯 Get Recommendations

```bash
curl http://localhost:5000/api/recommendations/1
```

### 4. 💬 Save Chat Message

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "userId": 1,
    "message": "Show me sports products",
    "response": "Here are top-rated sports items for you"
}'
```

### 5. 📜 Fetch Chat History

```bash
curl http://localhost:5000/api/chat/1
```

---

## 🧠 Agents Behind the Scenes

- **User Profile Agent**: Uses `users_with_embeddings.json`
- **Behavior Agent**: Uses `behavior_log.json` and checkout logs
- **Product Embedding Agent**: `generate_embeddings.py`
- **Recommendation Engine Agent**: Fetches based on vectors & purchase history
- **Chat Memory Agent**: Uses SQLite to store conversations

---

## 🛠 Tech Stack

- Python 3.10+
- Flask + SQLite + Firestore (optional)
- Ollama (`nomic-embed-text` model)
- JSON for data persistence

---

## 🔚 Final Notes

- You don’t need frontend for this hackathon.
- All testing can be done via terminal or tools like Postman.
- Ensure `ollama serve` is running during embedding generation.

Happy hacking! 💡
