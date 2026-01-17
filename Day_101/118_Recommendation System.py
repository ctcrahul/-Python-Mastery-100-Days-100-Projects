# Recommendation System (Collaborative Filtering)

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# LOAD DATA
# -----------------------------
data = pd.read_csv("ratings.csv")

# Create User-Item matrix
user_item = data.pivot_table(index="user_id", columns="item_id", values="rating").fillna(0)

# -----------------------------
# SIMILARITY MATRIX
# -----------------------------
