import os
import json
import datetime
from pathlib import Path

# Set up path to behavior log
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
BEHAVIOR_LOG = DATA_DIR / "behavior_log.json"

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

def log_behavior(user_id, product_id, event_type):
    timestamp = datetime.datetime.now().isoformat()
    behavior_entry = {
        "user_id": str(user_id),
        "product_id": str(product_id),
        "event_type": event_type,
        "timestamp": timestamp,
    }

    # Load existing logs
    if BEHAVIOR_LOG.exists():
        try:
            with open(BEHAVIOR_LOG, "r") as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            logs = []
    else:
        logs = []

    logs.append(behavior_entry)

    # Save back to file
    with open(BEHAVIOR_LOG, "w") as f:
        json.dump(logs, f, indent=2)

    print(f"[LOGGED] {event_type.upper()} | User: {user_id} | Product: {product_id} | Time: {timestamp}")

# CLI Interaction
if __name__ == "__main__":
    print("🧠 Behavior Logger")
    try:
        user_id = int(input("Enter User ID: "))
        product_id = int(input("Enter Product ID: "))
        event_type = input("Enter Event Type (e.g., view, click, buy): ").strip().lower()

        if event_type not in {"view", "click", "buy"}:
            raise ValueError("Unsupported event type.")

        log_behavior(user_id, product_id, event_type)
    except ValueError:
        print("❌ Invalid input. Make sure IDs are integers and event type is one of: view, click, buy.")
