#coding:utf-8
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from main import app
from ext import db
from models import User, Post, Tag, Comment

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def create_db():
	db.create_all()	

@manager.shell
def get_shell_context():
	return dict(app=app, db=db, User=User, Post=Post, Tag=Tag, Comment=Comment)

if __name__ == '__main__':
	manager.run()
