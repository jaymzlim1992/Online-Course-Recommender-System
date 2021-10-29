import os

# BASE DIRECTORY
basedir = os.path.abspath(os.path.dirname(__file__))


# CONFIGURATION FOR WEBAPP
class WebappConfig(object):

    # SECRET KEY
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A-VERY-LONG-SECRET-KEY'

    # DATABASE CONFIGURATION
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'database/app_database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# CONFIGURATION FOR RECOMMENDER MODULE
# DATA FILE PATH
tfidf_data_filepath = os.path.join(basedir, 'recommendation/featurematrix/tfidf_data.pickle')
categorical_data_filepath = os.path.join(basedir, 'recommendation/featurematrix/categorical_data.pickle')
tfidf_vectorizer_filepath = os.path.join(basedir, 'recommendation/featurematrix/tfidf_vectorizer.pickle')
# TEXT BASED RECOMMENDATION THRESHOLD
text_thres = 0
# MINIMUM FREE COURSE COUNT THRESHOLD
free_show_thres = 20
# RECOMMENDATION RESULTS SIZE
recommend_topn = 50
# DEFAULT POPULAR RESULTS SIZE
recommend_default_topn = 50
