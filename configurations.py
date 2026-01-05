class BaseConfig(object):
    '''
    Base config class
    '''
    DEBUG = True
    TESTING = False

class ProductionConfig(BaseConfig):
    """
    Production specific config
    """
    DEBUG = False

class DevelopmentConfig(BaseConfig):
    """
    Development environment specific configuration
    """
    DEBUG = True
    TESTING = True

    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
