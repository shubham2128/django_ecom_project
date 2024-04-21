import pickle
import pandas as pd
from django.conf import settings

def get_recommendations(data, user_id, top_n, algo):
    # Creating an empty list to store the recommended product ids
    recommendations = []
    # Creating an user item interactions matrix
    user_item_interactions_matrix = data.pivot(index='user_id', columns='prod_id', values='rating')
    # Extracting those product ids which the user_id has not interacted yet
    non_interacted_products = user_item_interactions_matrix.loc[user_id][user_item_interactions_matrix.loc[user_id].isnull()].index.tolist()
    # Looping through each of the product ids which user_id has not interacted yet
    for item_id in non_interacted_products:
        # Predicting the ratings for those non-interacted product ids by this user
        est = algo.predict(user_id, item_id).est
        # Appending the predicted ratings
        recommendations.append((item_id, est))
    # Sorting the predicted ratings in descending order
    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations[:top_n]  # Returning top n highest predicted rating products for this user

# Load the trained model from pickle file
with open(settings.MODEL_FILE, 'rb') as f:
    algo_knn_user = pickle.load(f)
df_final = pd.read_csv(settings.DATASET_FILE)
# Making top 5 recommendations for user_id "A3LDPF5FMB782Z" with a similarity-based recommendation engine
recommendations = get_recommendations(df_final, 'A3LDPF5FMB782Z', 5, algo_knn_user)

print(recommendations)
