#coding:utf-8
import os
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from webapp import create_app
from webapp.ext import db
from webapp.models import User, Post, Tag, Comment

env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app('webapp.config.%sConfig'%env.capitalize())

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('server', Server())
manager.add_command('db', MigrateCommand)

@manager.command
def create_db():
	db.create_all()	

@manager.shell
def get_shell_context():
	return dict(app=app, db=db, User=User, Post=Post, Tag=Tag, Comment=Comment)

if __name__ == '__main__':
	manager.run()
