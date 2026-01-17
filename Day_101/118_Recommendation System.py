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
similarity = cosine_similarity(user_item)
similarity_df = pd.DataFrame(similarity, index=user_item.index, columns=user_item.index)

# -----------------------------
# RECOMMEND FUNCTION
# -----------------------------
def recommend(user_id, top_n=3):
    similar_users = similarity_df[user_id].sort_values(ascending=False)[1:]
    weighted_ratings = user_item.loc[similar_users.index].T.dot(similar_users)
    recommendations = weighted_ratings.sort_values(ascending=False).head(top_n)
    return recommendations.index.tolist()
# -----------------------------
# TEST
# -----------------------------
if __name__ == "__main__":
    user = int(input("Enter user id: "))
    print("Recommended items:", recommend(user))
