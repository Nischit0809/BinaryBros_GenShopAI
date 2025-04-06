import json
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import os

# Load recommendations and users
with open("data/recommendations.json", "r") as f:
    recommendations = json.load(f)

with open("data/users.json", "r") as f:
    users = json.load(f)

# Ensure output directory exists
os.makedirs("exports", exist_ok=True)

# 1️⃣ Bar Chart: Most Recommended Categories
category_count = Counter()
for user_obj in recommendations:
    for rec in user_obj["recommendations"]:
        category_count[rec["category"]] += 1

plt.figure(figsize=(8, 5))
plt.bar(category_count.keys(), category_count.values(), color="skyblue")
plt.title("Top Recommended Categories")
plt.xlabel("Category")
plt.ylabel("Number of Recommendations")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("exports/top_recommended_categories.png")
plt.close()

# 2️⃣ Word Cloud: User Interests
all_interests = " ".join(user["interests"] for user in users)
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(all_interests)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.tight_layout()
plt.savefig("exports/user_interests_wordcloud.png")
plt.close()

# 3️⃣ Heatmap: User vs Categories
user_names = [user["name"] for user in users]
categories = list({rec["category"] for user_obj in recommendations for rec in user_obj["recommendations"]})

user_category_matrix = []
for user_obj in recommendations:
    user_name = next((u["name"] for u in users if u["user_id"] == user_obj["user_id"]), "Unknown")
    recs = user_obj["recommendations"]
    user_counts = Counter(rec["category"] for rec in recs)
    row = [user_counts.get(cat, 0) for cat in categories]
    user_category_matrix.append(row)

plt.figure(figsize=(10, 6))
sns.heatmap(user_category_matrix, annot=True, fmt="d", xticklabels=categories, yticklabels=user_names, cmap="Blues")
plt.title("User vs Recommended Categories")
plt.xlabel("Category")
plt.ylabel("User")
plt.tight_layout()
plt.savefig("exports/user_category_heatmap.png")
plt.close()

print("✅ Visualizations exported to the 'exports' folder.")
