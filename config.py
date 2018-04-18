#coding:utf-8
class Config(object):
	pass

class SomeConfig(object):
	pass

class DevConfig(Config):
	DEBUG = True
	SECRET_KEY = 'I am a ... what'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format('root', '123456', 'localhost', '3306', 'mastering')
