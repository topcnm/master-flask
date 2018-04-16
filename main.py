#coding:utf-8
from flask import Flask, g, request, session, make_response
from functools import wraps
import json
from config import DevConfig
from ext import db
from models import User
from random import randint

app = Flask(__name__)
app.config.from_object(DevConfig)
db.init_app(app)

@app.before_request
def before_request():
	if 'user_id' in session:
		print('i coming == {} =='.format(session['user_id']))
	
@app.errorhandler(404)
def api_not_found(error):
	return 'api 不存在'

# 登录要求
def login_required(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		if 'user_id' in session:
			return func(*args, **kwargs)
		else:
			rps = { 'success': False, 'result': None  }
			return make_response(json.dumps(rps), 401)		

	return wrapper

@app.route("/blog/login", methods=['post'])
def login():
	params = request.get_json()
	username = params['username']
	password = params['password']
	user = User.query.filter(User.username == username, User.password == password).first()
	rps = { 'success': False, 'result': None  }
	if user:
		session['user_id'] = user.id
		rps['success'] = True
		rps['result'] = {
			'username': user.username, 
			'id': user.id
		} 
		resp = make_response(json.dumps(rps), 200)
		print('denglu cg')
		return resp
	return json.dumps(rps)

@app.route("/blog/logout", methods=['post'])
@login_required
def logout():
	session.pop('user_id')
	return make_response(json.dumps({'success': True}), 200)	

@app.route("/blog/search/<pageNo>")
@login_required
def get_user(pageNo):
	return '验证页面（必须登录）第（{}）页 '.format(pageNo)

if __name__ == '__main__':
	app.run()
