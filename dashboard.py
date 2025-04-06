import json
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
import seaborn as sns
import pandas as pd

# Load data
with open("data/recommendations.json", "r") as f:
    recommendations = json.load(f)

with open("data/users.json", "r") as f:
    users = json.load(f)

# ---------- 1. Top Recommended Categories ----------
category_counter = Counter()
for rec in recommendations:
    for item in rec["recommendations"]:
        category_counter[item["category"]] += 1

top_categories = category_counter.most_common()

# Plot bar chart
plt.figure(figsize=(10, 5))
plt.bar(*zip(*top_categories))
plt.title("Top Recommended Categories")
plt.xlabel("Category")
plt.ylabel("Recommendation Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ---------- 2. Word Cloud for Interests ----------
all_interests = " ".join([u["interests"] for u in users])
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_interests)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("User Interests Word Cloud")
plt.show()

# ---------- 3. Heatmap: User vs Category ----------
# Create a matrix of user vs category count
user_names = [u["name"] for u in users]
all_categories = list({item["category"] for rec in recommendations for item in rec["recommendations"]})
data_matrix = []

for rec in recommendations:
    row = []
    rec_categories = [r["category"] for r in rec["recommendations"]]
    for cat in all_categories:
        row.append(rec_categories.count(cat))
    data_matrix.append(row)

df = pd.DataFrame(data_matrix, index=user_names, columns=all_categories)

plt.figure(figsize=(10, 6))
sns.heatmap(df, annot=True, cmap="YlGnBu", linewidths=0.5)
plt.title("User vs Recommended Categories")
plt.xlabel("Category")
plt.ylabel("User")
plt.tight_layout()
plt.show()
