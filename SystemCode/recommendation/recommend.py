# Recommendation module
# Takes user input and returns a sorted list of recommended courses.

# Initialize Library Setup
import pickle
from sklearn.metrics.pairwise import cosine_similarity

from SystemCode.recommendation import utils
from SystemCode.config import basedir
from SystemCode.config import alpha
from SystemCode.config import batch_size


# Recommend Function
def recommend(user_input, rating_data):
    # 1. Feature Extraction - Text Based (TfIdf)
    # Load Tfidf Data Sparse Matrix
    tfidf_data_filepath = basedir + '/recommendation/featurematrix/tfidf_data.pickle'
    tfidf_data_file = open(tfidf_data_filepath, 'rb')
    tfidf_data = pickle.load(tfidf_data_file)
    tfidf_data_file.close()
    # Text Input and Similarity Score
    text_input = user_input[0]
    text_processed = utils.text_preprocess(text_input)
    tfidf_vect = utils.tfidf_vectorize(text_processed)
    tfidf_sim = cosine_similarity(tfidf_vect, tfidf_data).ravel()

    # 2. Feature Extraction - Categorical Based (One-Hot Encoded)
    # Load Categorical One-Hot Encoded Sparse Matrix
    categorical_data_filepath = basedir + '/recommendation/featurematrix/categorical_data.pickle'
    categorical_data_file = open(categorical_data_filepath, 'rb')
    categorical_data = pickle.load(categorical_data_file)
    categorical_data_file.close()
    # Categroical Input and Similarity Score
    categorical_input = user_input[1:]
    categorical_vect = utils.categorical_encode(categorical_input)
    categorical_sim = utils.cond_sim(categorical_vect, categorical_data).ravel()

    # 3. Calculate Weighted Similarity Score
    w1 = alpha
    w2 = round(1 - w1, 2)
    sim = (w1 * tfidf_sim) + (w2 * categorical_sim)

    # 4. Sort Similarity and Filter by Threshold
    sim_thres = w2
    sorted_id = utils.sortnfilter(sim, sim_thres)
    sorted_sim = sim[sorted_id]

    # 5. Apply Batch Ranking using rating data
    rec_id = utils.batch_rank(sorted_id, rating_data, batch_size)

    return sorted_sim, sorted_id, rec_id
