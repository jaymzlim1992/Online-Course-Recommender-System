# Recommendation module
# Takes user input and returns a sorted list of recommended courses.

# Initialize Library Setup
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
    categorical_input = user_input[1:3]
    categorical_vect = utils.categorical_encode(categorical_input)
    categorical_sim = utils.cond_sim(categorical_vect, categorical_data[:, :-1]).ravel()

    # 3. Recommendation Masks (Free vs Paid Courses Masks)
    free_option_ind = user_input[-1]
    free_option_data = categorical_data[:, -1]
    thres_mask = (tfidf_sim > config.text_thres)
    if free_option_ind == 1:
        free_mask = ((free_option_data == 1) * thres_mask) == 1
    else:
        free_mask = (np.ones(tfidf_data.shape[0]) * thres_mask) == 1
    paid_mask = ((np.ones(tfidf_data.shape[0]) * thres_mask) - free_mask) == 1

    # 4. Apply Masks and Rank by categorical_sim group and rating
    rec_sim, rec_idx = utils.ranking(free_mask, tfidf_sim, categorical_sim, rating_data)

    # 5. Append paid courses if number of free courses below a threshold
    if (free_mask.sum() < config.free_show_thres) and (paid_mask.sum() > 0):
        paid_sim, paid_idx = utils.ranking(paid_mask, tfidf_sim, categorical_sim, rating_data)
        rec_sim = np.append(rec_sim, paid_sim)
        rec_idx = np.append(rec_idx, paid_idx)

    # 6. Convert Index to courseID
    rec_idx = rec_idx + 1
    course_sim = rec_sim[:config.recommend_topn].tolist()
    course_idx = rec_idx[:config.recommend_topn].tolist()

    return course_idx


def recommend_default(rating_data):
    sort_idx = (np.argsort(rating_data)[::-1])
    sort_course = sort_idx[:config.recommend_default_topn]
    default_course = [int(x+1) for x in sort_course]
    return default_course
