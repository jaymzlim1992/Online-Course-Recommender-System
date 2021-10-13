# Utility functions for recommendation module

# Initialize Library Setup
import numpy as np
import re
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from SystemCode import config


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
    encode = np.zeros((1, 6))
    # Binary Encode Course Duration (0 - No Preference, 1 - Short, 2 - Medium, 3 - Long)
    if categorical_input[0] > 0:
        encode[0, categorical_input[0] - 1] = 1
    # Binary Encode Course Difficulty (0 - No Preference, 1 - Introductory, 2 - Intermediate, 3 - Advanced)
    if categorical_input[1] > 0:
        encode[0, categorical_input[1] + 2] = 1
    return encode


# 3) TfIdf Vectorizer:
# Takes list of tokens as input and apply TfIdf Vectorization based on the pretrained dictionary.
def tfidf_vectorize(text, vectorizer):
    # Load Tfidf Vectorizer
    # vectorizer_file = open(config.tfidf_vectorizer_filepath, 'rb')
    # vectorizer = pickle.load(vectorizer_file)
    # vectorizer_file.close()
    tfidf = vectorizer.transform([text])
    return tfidf


# 4) Cosine Similarity:
# Takes 2 vectors and calculate cosine similarity
def cond_sim(input_vec, data_vec):
    input_durr = input_vec[:, :3]
    input_diff = input_vec[:, 3]
    data_durr = data_vec[:, :3]
    data_diff = data_vec[:, 3]
    if (input_diff.sum() + input_durr.sum()) == 0:
        sim = np.ones(data_vec.shape[0])
    elif input_durr.sum() == 0:
        sim = cosine_similarity(input_diff, data_diff)
    elif input_diff.sum() == 0:
        sim = cosine_similarity(input_durr, data_durr)
    else:
        sim = cosine_similarity(input_vec, data_vec)
    return sim


# 5) Ranking based on popularity index
# Given a sorted and threshold filtered ID of recommendations
# Batch rank for every batch_size of ID by rating.
def ranking(mask, text_sim, categorical_sim, rating):
    target_idx = np.arange(text_sim.shape[0])[mask]
    target_text_sim = text_sim[mask]
    target_categorical_sim = categorical_sim[mask]
    target_rating = rating[mask]
    target_scores = sorted(np.unique(target_categorical_sim), reverse=True)
    rec_idx = np.array([], dtype=int)
    rec_sim = np.array([])
    for score in target_scores:
        group_mask = (target_categorical_sim == score)
        group_idx = target_idx[group_mask]
        group_text_sim = target_text_sim[group_mask]
        group_rating = target_rating[group_mask]
        group_sort_idx = np.argsort(group_rating)[::-1]
        rec_idx = np.append(rec_idx, group_idx[group_sort_idx])
        rec_sim = np.append(rec_sim, group_text_sim[group_sort_idx])
    return rec_sim, rec_idx


# 6) Load-up Pickle Object Data Files
def load_pickle(filename):
    data_file = open(filename, 'rb')
    data = pickle.load(data_file)
    data_file.close()
    return data
