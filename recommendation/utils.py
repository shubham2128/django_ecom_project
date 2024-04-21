from collections import defaultdict
from surprise import accuracy
from django.conf import settings
import pandas as pd
import pickle

def get_recommendations(user_id, top_n=5):
    # Load the dataset
    print(settings.DATASET_FILE)
    df_final = pd.read_csv(settings.DATASET_FILE)
    columns_name = ['user_id','prod_id','rating','timestamp']
    df_final.columns=columns_name
    print(df_final.columns) # Debug print to check column names
    # Load the trained model from pickle file
    with open(settings.MODEL_FILE, 'rb') as f:
        algo_knn_user = pickle.load(f)

    # Create an empty list to store the recommended product ids
    recommendations = []

    # Creating an user item interactions matrix
    user_item_interactions_matrix = df_final.pivot(index='user_id', columns='prod_id', values='rating')

    # Extracting those product ids which the user_id has not interacted yet
    non_interacted_products = user_item_interactions_matrix.loc[user_id][user_item_interactions_matrix.loc[user_id].isnull()].index.tolist()

    # Looping through each of the product ids which user_id has not interacted yet
    for item_id in non_interacted_products:

        # Predicting the ratings for those non-interacted product ids by this user
        est = algo_knn_user.predict(user_id, item_id).est

        # Appending the predicted ratings
        recommendations.append((item_id, est))

    # Sorting the predicted ratings in descending order
    recommendations.sort(key=lambda x: x[1], reverse=True)

    return recommendations[:top_n]  # Returning top n highest predicted rating products for this user
