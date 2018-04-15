#coding:utf-8
class Config(object):
	pass

class DevConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format('root', '123456', 'localhost', '3306', 'mastering')
