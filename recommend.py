# Recommendation module
# Takes user input and returns a sorted list of recommended courses.

# Initialize Library Setup

from helpers import *


def recommend(user_input, rating_data, tfidf_weight, sim_thres, rank_batch_size):
    text_input = user_input[0]
    categorical_input = user_input[1:]

    # Text Based Feature Extraction - TfIdf
    processed_text = text_preprocess(text_input)
    tfidf = tfidf_vectorize(processed_text)

    # Categorical Data Feature Extraction
    categorical = categorical_encode(categorical_input)

    # Calculate Text Based Feature Similarity Score
    tfidf_data_filepath = 'feature_data/tfidf_feature.pickle'
    tfidf_data = pickle.load(open(tfidf_data_filepath, 'rb'))
    tfidf_sim = cal_sim(tfidf, tfidf_data)

    # Calculate Categorical Feature Similarity Score
    categorical_data_filepath = 'feature_data/cat_feature.pickle'
    categorical_data = pickle.load(open(categorical_data_filepath, 'rb'))
    categorical_sim = cal_sim(categorical, categorical_data)

    # Combined Similarity Score
    w1 = tfidf_weight
    w2 = 1 - w1
    sim = w1 * tfidf_sim + w2 * categorical_sim

    # Sort Course ID by similarity score and threshold
    sorted_id = sortnfilter(sim, sim_thres)

    # Apply Batch Ranking using rating data
    rec_id = batch_rank(sorted_id, rating_data, rank_batch_size)

    return rec_id


df = pd.read_csv('feature_data/Edx_Data.csv')
rating = df['Rating']
tryinput = ['python', 0, 2, 1]
tryoutput = recommend(tryinput, rating, 0.8, 0.2, 10)
print(tryoutput.shape)
print(tryoutput)
