# Helper functions for recommendation module
# Initialize Library Setup

import numpy as np
import pandas as pd
import re
import spacy
import pickle
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity


# 1) Text Preprocessing
# Takes any rawtext as input and apply text preprocessing:
#  - remove all non-ASCII characters
#  - lower-casing all text
#  - apply spacy preprocessing pipeline and extract word with tags PROPN, NOUN, VERB
#  - return list of lemmatized tokens

def text_preprocess(rawtext):
    tokens = []
    tags = ['PROPN', 'NOUN', 'VERB']
    nlp = spacy.load('en_core_web_md')

    text = re.sub('([^\x00-\x7F])+', '', rawtext)
    text = text.lower()
    doc = nlp(text)
    for token in doc:
        if token.pos_ in tags:
            tokens.append(token.lemma_)
    return np.array(tokens)


# 2) Encoding User Input Features:
# Takes list of categorical data (course difficulty, course duration and course free option) as input
# Returns one-hot encoded features.

def categorical_encode(categorical_input):
    encode = np.zeros((1, 8))
    # Binary Encode Course Difficulty (0 - Introductory, 1 - Intermediate, 2 - Advanced)
    if not(pd.isna(categorical_input[0])):
        encode[0, categorical_input[0]] = 1
    # Binary Encode Course Duration (0 - Short, 1 - Medium, 2 - Long)
    if not(pd.isna(categorical_input[1])):
        encode[0, categorical_input[1] + 3] = 1
    # Binary Encode Course Free Option Availability (0 - No, 1 - Yes)
    if not(pd.isna(categorical_input[2])):
        encode[0, categorical_input[2] + 6] = 1
    return encode


# 3) TfIdf Vectorizer:
# Takes list of tokens as input and apply TfIdf Vectorization based on the pretrained dictionary.
df_dict_filepath = 'feature_data/df_dict.pickle'
tfidf_feature_filepath = 'feature_data/tfidf_feature.pickle'


def tfidf_vectorize(tokens):
    tfidf_feature = pickle.load(open(tfidf_feature_filepath, 'rb'))
    num_doc = tfidf_feature.shape[0]

    df_dict = pickle.load(open(df_dict_filepath, 'rb'))
    df_dict_vocab = list(df_dict.keys())
    df_dict_size = len(df_dict_vocab)

    tfidf = np.zeros((1, df_dict_size))
    counter = Counter(tokens)
    for word in list(counter.keys()):
        if word in df_dict_vocab:
            tf = counter[word]/len(tokens)
            idf = np.log(num_doc / (df_dict[word] + 1)) + 1  # Adding 1's to avoid division with 0
            tfidf[0, df_dict_vocab.index(word)] = tf * idf
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
    # Sort
    sort_idx = np.argsort(sim_scores)[::-1]
    sim_sorted = sim_scores[sort_idx]

    # Filters score that are above threshold
    sort_idx_filtered = sort_idx[sim_sorted > thres]

    return sort_idx_filtered


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
