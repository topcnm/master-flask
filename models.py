#coding:utf-8
from ext import db

class User(db.Model):
        __tablename__ = 'user'
        __table_args__ = {
                'mysql_charset': 'utf8'
        }
        id = db.Column(db.Integer, primary_key = True, autoincrement = True)
        username = db.Column(db.String(64), nullable = False)
        password = db.Column(db.String(64), nullable = False)

        posts = db.relationship('Post', backref='user', lazy='dynamic')

tags = db.Table('post_tags',db.Column('post_id', db.Integer, db.ForeignKey('post.id')),db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))

class Post(db.Model):
        __tablename = 'post'
        __table_args__ = {
                'mysql_charset': 'utf8'
        }
        id = db.Column(db.Integer, primary_key = True, autoincrement = True)
        title = db.Column(db.String(64))
        text = db.Column(db.Text)
        publish_data = db.Column(db.DateTime)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        comments = db.relationship('Comment', backref='post', lazy='dynamic')

        tags = db.relationship('Tag', secondary=tags, backref='posts', lazy='dynamic')

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
