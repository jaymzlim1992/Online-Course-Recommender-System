# Helper functions for recommendation module
# Initialize Library Setup

import numpy as np
import re
import pickle

from sklearn.metrics.pairwise import cosine_similarity

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# 1) Text Preprocessing
# Initilization
stopwordsdic = stopwords.words('english')
lemmatizer = WordNetLemmatizer()


# Takes any rawtext as input and apply text preprocessing:
#   - remove all non-ASCII characters
#   - lower-casing all text and remove unecessary spaces
#   - remove punctuations
#   - remove stopwords
#   - lemmatize words
#   - create bag-of-words (bow) strings
def text_preprocess(rawtext):
    text = re.sub('([^\x00-\x7F])+', '', rawtext)  # Remove all non ASCII characters
    text = text.lower()  # lower casing all words
    text = text.strip()  # Remove White Spaces
    text = re.sub('[^A-Za-z0-9]+', ' ', text)  # Remove Punctuations
    text = word_tokenize(text)  # Tokenize
    text = [word for word in text if word not in stopwordsdic]  # Remove stopwords
    text = [lemmatizer.lemmatize(word) for word in text]  # Lemmatize words
    bow = ' '.join(text)  # Create Bag-of-Words
    return bow


# 2) Encoding User Input Features:
# Takes list of categorical data (course difficulty, course duration and course free option) as input
# Returns one-hot encoded features.
def categorical_encode(categorical_input):
    encode = np.zeros((1, 8))
    # Binary Encode Course Difficulty (0 - No Preference, 1 - Introductory, 2 - Intermediate, 3 - Advanced)
    if categorical_input[0] > 0:
        encode[0, categorical_input[0] - 1] = 1
    # Binary Encode Course Duration (0 - No Preference, 1 - Short, 2 - Medium, 3 - Long)
    if categorical_input[1] > 0:
        encode[0, categorical_input[1] + 2] = 1
    # Binary Encode Course Free Option Availability (0 - No, 1 - Yes)
    encode[0, categorical_input[2] + 6] = 1
    return encode


# 3) TfIdf Vectorizer:
# Takes list of tokens as input and apply TfIdf Vectorization based on the pretrained dictionary.
def tfidf_vectorize(text):
    # Load Tfidf Vectorizer
    tfidf_vectorizer_filepath = './feature_data/tfidf_vectorizer.pickle'
    vectorizer_file = open(tfidf_vectorizer_filepath, 'rb')
    vectorizer = pickle.load(vectorizer_file)
    vectorizer_file.close()
    tfidf = vectorizer.transform([text])
    return tfidf


# 4) Cosine Similarity:
# Takes 2 vectors and calculate cosine similarity
def cal_sim(input_vec, data_vec):
    sim = cosine_similarity(input_vec, data_vec).ravel()
    return sim


# 5) Sorting Similarity Score and Filters score above threshold:
# Sort a list of similarity score in descending order.
# Filters score that above threshold
# Returns course IDs
def sortnfilter(sim_scores, thres):
    # Sort similarity score in descending order
    sort_idx = np.argsort(sim_scores)[::-1]
    sim_sorted = sim_scores[sort_idx]
    # Filters score that are above threshold
    sort_idx_thres = sort_idx[sim_sorted > thres]
    return sort_idx_thres


# 6) Batch Ranking
# Given a sorted and threshold filtered ID of recommendations
# Batch rank for every batch_size of ID by rating.
def batch_rank(sort_filtered_id, rating, batch_size):
    num_batch = int(len(sort_filtered_id) / batch_size) + (len(sort_filtered_id) % batch_size > 0)
    ranked = np.array([])

    for i in range(num_batch):
        batch_id = sort_filtered_id[i*batch_size:min((i+1)*batch_size, len(sort_filtered_id))]
        batch_rating = rating[batch_id]
        batch_sort_idx = np.argsort(batch_rating)[::-1]
        ranked_batch_id = batch_id[batch_sort_idx]
        ranked = np.append(ranked, ranked_batch_id).astype(int)

    return ranked
