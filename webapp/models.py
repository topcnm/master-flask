#coding:utf-8
from ext import db, bcrypt
import datetime

class User(db.Model):
        __tablename__ = 'user'
        __table_args__ = {
                'mysql_charset': 'utf8'
        }
        id = db.Column(db.Integer, primary_key = True, autoincrement = True)
        username = db.Column(db.String(64), unique = True, nullable = False)
        password = db.Column(db.String(64), nullable = False)

        posts = db.relationship('Post', backref='user', lazy='dynamic')
	albums = db.relationship('Album', backref='user', lazy='dynamic')
	pictures = db.relationship('Picture', backref='user', lazy='dynamic')

	def __init__(self, username):
		self.username = username
	
	def set_password(self, password):
		self.password = bcrypt.generate_password_hash(password)

	def check_password(self, password):
		return bcrypt.check_password_hash(self.password, password)		

	@staticmethod
	def get_user_by_username_and_password(username, password):
		user = User.query.filter(User.username == username).first()
		if user:
			if user.check_password(password):
				return user
			else:
				return None
		else:
			return None
'''
tags = db.Table('post_tags',db.Column('post_id', db.Integer, db.ForeignKey('post.id')),db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))
'''

class Post(db.Model):
        __tablename = 'post'
        __table_args__ = {
                'mysql_charset': 'utf8'
        }
        id = db.Column(db.Integer, primary_key = True, autoincrement = True)
        title = db.Column(db.String(64))
     	text = db.Column(db.Text)
        publish_date = db.Column(db.DateTime, default=datetime.datetime.now)
	publish_able = db.Column(db.String(1))
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))

        comments = db.relationship('Comment', backref='post', lazy='dynamic')

	def __init__(self, title, text, publish_able, tag_id):
		self.title = title
		self.text = text
		self.publish_able = publish_able		
		self.tag_id = tag_id	

        def __repr__(self):
                return '<Post {}>'.format(self.title)

class Tag(db.Model):
        __tablename__ = 'tag'
        __table_args__ = {
                'mysql_charset': 'utf8'
        }
        id = db.Column(db.Integer, primary_key = True, autoincrement = True)
        title = db.Column(db.String(255), nullable = False)
	remark = db.Column(db.String(255))
       	
	posts = db.relationship('Post', backref='tag', lazy='dynamic')

	def __repr__(self):
                return "<Tag '{}'>".format(self.title)

class Comment(db.Model):
        __tablename__ = 'comment'
        __table_args__ = {
                'mysql_charset': 'utf8'
        }
        id = db.Column(db.Integer, primary_key = True, autoincrement = True)
        name = db.Column(db.String(255), nullable = False)
        text = db.Column(db.Text(), nullable = False)
        date = db.Column(db.DateTime())
	remark = db.Column(db.String(255))
        post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

        def __repr__(self):
                return "<Comment '{}'>".format(self.text[:15])


class Album(db.Model):
	__tablename__ = 'album'
	__table_args__ = {
		'mysql_charset': 'utf8'
	}
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	title = db.Column(db.String(64), nullable = False)
	remark = db.Column(db.String(255), nullable = False)
	front = db.Column(db.String(255))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	pictures = db.relationship('Picture', backref='album', lazy='dynamic')

class Picture(db.Model):
	__tablename__ = 'picture'
	__table_args__ = {
		'mysql_charset': 'utf8'
	}
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	remark = db.Column(db.String(255))
	full_link = db.Column(db.String(255))
	tiny_link = db.Column(db.String(255))
	album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
