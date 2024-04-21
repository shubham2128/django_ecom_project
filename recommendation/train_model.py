import warnings
from collections import defaultdict
from surprise.prediction_algorithms.knns import KNNBasic
from surprise import Dataset, Reader, accuracy
from surprise.model_selection import train_test_split, GridSearchCV
import pandas as pd
import pickle
warnings.filterwarnings('ignore')

# Loading the dataset and performing pre-processing
amazon = pd.read_csv('ratings_Electronics.csv', header=None)
amazon.columns = ['user_id', 'prod_id', 'rating', 'timestamp']
amazon.drop(['timestamp'], axis=1, inplace=True)
df = amazon.copy()

# Filtering users and products based on rating count thresholds
ratings_count_user = df['user_id'].value_counts()
ratings_count_prod = df['prod_id'].value_counts()
# Ratings thresholds
RATINGS_CUTOFF_USER = 50
RATINGS_CUTOFF_PROD = 5

remove_users = ratings_count_user[ratings_count_user < RATINGS_CUTOFF_USER].index
remove_prods = ratings_count_prod[ratings_count_prod < RATINGS_CUTOFF_PROD].index

df_final = df[~df['user_id'].isin(remove_users)]
df_final = df_final[~df_final['prod_id'].isin(remove_prods)]

# Loading the dataset into Surprise
reader = Reader(rating_scale=(1, 5))
df_surprise = Dataset.load_from_df(df_final[['user_id', 'prod_id', 'rating']], reader)

# Splitting data into train and test sets
trainset, testset = train_test_split(df_surprise, test_size=0.7, random_state=42)

# Initializing KNNBasic model
sim_options = {'name': 'cosine', 'user_based': True}
algo_knn_user = KNNBasic(sim_options=sim_options, verbose=False, random_state=1)

# Fitting the model on the training data
algo_knn_user.fit(trainset)

def precision_recall_at_k(model, k=10, threshold=3.5):
    """Return precision and recall at k metrics for each user"""

    # First map the predictions to each user
    user_est_true = defaultdict(list)

    # Making predictions on the test data
    predictions = model.test(testset)

    for uid, _, true_r, est, _ in predictions:
        user_est_true[uid].append((est, true_r))

    precisions = dict()
    recalls = dict()
    for uid, user_ratings in user_est_true.items():

        # Sort user ratings by estimated value
        user_ratings.sort(key=lambda x: x[0], reverse=True)

        # Number of relevant items
        n_rel = sum((true_r >= threshold) for (_, true_r) in user_ratings)

        # Number of recommended items in top k
        n_rec_k = sum((est >= threshold) for (est, _) in user_ratings[:k])

        # Number of relevant and recommended items in top k
        n_rel_and_rec_k = sum(((true_r >= threshold) and (est >= threshold))
                              for (est, true_r) in user_ratings[:k])

        # Precision@K: Proportion of recommended items that are relevant
        # When n_rec_k is 0, Precision is undefined. Therefore, we are setting Precision to 0 when n_rec_k is 0
        precisions[uid] = n_rel_and_rec_k / n_rec_k if n_rec_k != 0 else 0

        # Recall@K: Proportion of relevant items that are recommended
        # When n_rel is 0, Recall is undefined. Therefore, we are setting Recall to 0 when n_rel is 0
        recalls[uid] = n_rel_and_rec_k / n_rel if n_rel != 0 else 0

    # Mean of all the predicted precisions are calculated.
    precision = round((sum(prec for prec in precisions.values()) / len(precisions)), 3)

    # Mean of all the predicted recalls are calculated.
    recall = round((sum(rec for rec in recalls.values()) / len(recalls)), 3)

    accuracy.rmse(predictions)

    print('Precision: ', precision)  # Command to print the overall precision
    print('Recall: ', recall)  # Command to print the overall recall
    print('F_1 score: ', round((2 * precision * recall) / (precision + recall), 3))  # Formula to compute the F-1 score

# Computing precision, recall, and F1 score for the model
precision_recall_at_k(algo_knn_user)

# Save the trained model to a pickle file
with open('knn_model.pkl', 'wb') as f:
    pickle.dump(algo_knn_user, f)
