#coding:utf-8
from flask_script import Manager
from main import app, User, Post, db, Tag, Comment

manager = Manager(app)

@manager.command
def say_hello():
	return ('Hello Moto')

@manager.shell
def get_shell_context():
	return dict(app=app, db=db, User=User, Post=Post, Tag=Tag, Comment=Comment)

if __name__ == '__main__':
	manager.run()
