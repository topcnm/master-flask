# coding:utf-8
class Config(object):
    pass


class ProConfig(object):
    DEBUG = False
    SECRET_KEY = 'I am a ... what'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
        'root', '123456', 'localhost', '3306', 'mastering')


class DevConfig(Config):
    DEBUG = True
    SECRET_KEY = 'I am a ... what'
    MAX_CONTENT_LENGTH = 1920 * 1080
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
        'root', '123456', 'localhost', '3306', 'mastering')
