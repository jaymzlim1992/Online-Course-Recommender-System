import os

# BASE DIRECTORY
basedir = os.path.abspath(os.path.dirname(__file__))


# CONFIGURATION FOR WEBAPP
class Config(object):

    # SECRET KEY
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A-VERY-LONG-SECRET-KEY'

    # DATABASE CONFIGURATION
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'database/app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# CONFIGURATION FOR RECOMMENDER MODULE
# TEXT BASED RECOMMENDATION WEIGHT
alpha = 0.8
# BATCH RANKING SIZE
batch_size = 10
