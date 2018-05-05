# coding:utf-8
from flask_script import Manager
from webapp.ext import db
from webapp.models import Tag

InitManager = Manager()

# init tag table to aviod post creation error


@InitManager.command
def init_tag():
    tag1 = Tag(title='common', remark='通用')
    tag2 = Tag(title='trip', remark='旅行')
    tag3 = Tag(title='life', remark='生活')
    tag4 = Tag(title='motion', remark='情感')

    db.session.add(tag1)
    db.session.add(tag2)
    db.session.add(tag3)
    db.session.add(tag4)

    db.session.commit()
