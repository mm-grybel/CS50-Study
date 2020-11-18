import os
basedir = os.path.abspath(os.path.dirname(__file__))


DATABASE_URL = os.environ.get('DATABASE_URL') or 'postgresql:///cs50-final'


class Config:
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    QUESTIONS_PER_PAGE = 8

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql:///cs50-final'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'postgresql:///cs50-final-test'


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URL') or 'postgresql:///cs50-final-prod'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}