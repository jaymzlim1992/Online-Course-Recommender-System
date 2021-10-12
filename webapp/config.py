import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    # SECRET KEY
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A-VERY-LONG-SECRET-KEY'


    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
