# Recommendation module
# Takes user input and returns a sorted list of recommended courses.

# Initialize Library Setup
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from SystemCode.recommendation import utils
from SystemCode import config


# Recommend Function
def recommend(user_input, rating_data, tfidf_vectorizer, tfidf_data, categorical_data):
    # 1. Feature Extraction - Text Based (TfIdf)
    # Load Tfidf Data Sparse Matrix
    # tfidf_data_file = open(config.tfidf_data_filepath, 'rb')
    # tfidf_data = pickle.load(tfidf_data_file)
    # tfidf_data_file.close()
    # Text Input and Similarity Score
    text_input = user_input[0]
    text_processed = utils.text_preprocess(text_input)
    tfidf_vect = utils.tfidf_vectorize(text_processed, tfidf_vectorizer)
    tfidf_sim = cosine_similarity(tfidf_vect, tfidf_data).ravel()

    # 2. Feature Extraction - Categorical Based (One-Hot Encoded)
    # Load Categorical One-Hot Encoded Sparse Matrix

    # categorical_data_file = open(config.categorical_data_filepath, 'rb')
    # categorical_data = pickle.load(categorical_data_file)
    # categorical_data_file.close()
    # Categroical Input and Similarity Score
    categorical_input = user_input[1:]
    categorical_vect = utils.categorical_encode(categorical_input)
    categorical_sim = utils.cond_sim(categorical_vect, categorical_data).ravel()

    # 3. Calculate Weighted Similarity Score
    w1 = config.alpha
    w2 = round(1 - w1, 2)
    sim = (w1 * tfidf_sim) + (w2 * categorical_sim)

    # 4. Sort Similarity and Filter by Threshold
    sim_thres = w2
    sorted_id = utils.sortnfilter(sim, sim_thres)
    sorted_sim = sim[sorted_id]

    # 5. Apply Batch Ranking using rating data
    rec_id = utils.batch_rank(sorted_id, rating_data, config.batch_size)[:config.recommend_topn]

    return sorted_sim, sorted_id, rec_id


def recommend_default(rating_data):
    sort_idx = (np.argsort(rating_data)[::-1])
    sort_course = sort_idx[:config.recommend_default_topn]
    default_course = [int(x+1) for x in sort_course]
    return default_course
