import firebase_admin
from firebase_admin import credentials, firestore
import os

# Correct path to service account key in config folder
key_path = os.path.join(os.path.dirname(__file__), "config", "firebase-adminsdk-key.json")

# Initialize the app only if it hasn't been already
if not firebase_admin._apps:
    cred = credentials.Certificate(key_path)
    firebase_admin.initialize_app(cred)

# Initialize Firestore DB
db = firestore.client()
