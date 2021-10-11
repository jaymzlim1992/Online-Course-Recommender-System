# Recommendation module
# Takes user input and returns a sorted list of recommended courses.

# Initialize Library Setup

from helpers import *
import pandas as pd
import pickle
import sqlite3
import time
from sklearn.metrics.pairwise import cosine_similarity


def recommend(user_input, rating_data, tfidf_weight, sim_thres, rank_batch_size):
    # 1. Feature Extraction - Text Based (TfIdf)
    # Load Tfidf Data Sparse Matrix
    tfidf_data_filepath = './feature_data/tfidf_data.pickle'
    tfidf_data_file = open(tfidf_data_filepath, 'rb')
    tfidf_data = pickle.load(tfidf_data_file)
    tfidf_data_file.close()
    # Text Input and Similarity Score
    text_input = user_input[0]
    text_processed = text_preprocess(text_input)
    tfidf_vect = tfidf_vectorize(text_processed)
    tfidf_sim = cosine_similarity(tfidf_vect, tfidf_data).ravel()

    # 2. Feature Extraction - Categorical Based (One-Hot Encoded)
    # Load Categorical One-Hot Encoded Sparse Matrix
    categorical_data_filepath = './feature_data/categorical_data.pickle'
    categorical_data_file = open(categorical_data_filepath, 'rb')
    categorical_data = pickle.load(categorical_data_file)
    categorical_data_file.close()
    # Categroical Input and Similarity Score
    categorical_input = user_input[1:]
    categorical_vect = categorical_encode(categorical_input)
    categorical_sim = cond_sim(categorical_vect, categorical_data).ravel()

    # 3. Calculate Weighted Similarity Score
    w1 = tfidf_weight
    w2 = round(1 - w1, 2)
    sim = (w1 * tfidf_sim) + (w2 * categorical_sim)

    # 4. Sort Similarity and Filter by Threshold
    sorted_id = sortnfilter(sim, sim_thres)
    sorted_sim = sim[sorted_id]

    # 5. Apply Batch Ranking using rating data
    rec_id = batch_rank(sorted_id, rating_data, rank_batch_size)

    return sorted_sim, sorted_id, rec_id


filename = './feature_data/Course_Database.db'
table_name = 'Course_Info'
sqlite_conn = sqlite3.connect(filename)
# Query Table
rawrating = pd.read_sql('SELECT "Popularity Index" FROM ' + table_name, sqlite_conn)
rating = rawrating.to_numpy().reshape(len(rawrating))
sqlite_conn.close()


start = time.time()
tryinput = ['python', 0, 0, 1]
trysim, tryoutput, tryid = recommend(tryinput, rating, 0.8, 0.2, 10)
print(tryoutput.shape)
print(trysim[:10])
print(tryoutput[:10])
print(time.time()-start)

