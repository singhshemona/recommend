import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '2344388cb0269cbe1d2a7c23dae8c64a9762f0838f63eed7f48'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ''' calling init_app on the extensions completes their initialization '''
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')



'''logging of lesser messages'''
class HerokuConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # # log to stderr
        # import logging
        # from logging import StreamHandler
        # file_handler = StreamHandler()
        # file_handler.setLevel(logging.INFO)
        # app.logger.addhandler(file_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku' : HerokuConfig,

    'default': DevelopmentConfig
}




#export DEV_DATABASE_URL= 'mysql+mysqlconnector://taniya:tansin@localhost/wrec'