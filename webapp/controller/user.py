#coding:utf-8
from flask import session, request, Response, Blueprint, make_response
import json
import copy
from webapp.ext import db
from webapp.models import User
from util import error_response, login_required

user = Blueprint('user', __name__)

@user.route("/login", methods=['post'])
def login():
	params = request.get_json()
	user = User.get_user_by_username_and_password(params['username'],params['password'])
	rps = copy.deepcopy(error_response)
	if user:
		session['user_id'] = user.id
		rps['success'] = True
		rps['result'] = {
			'username': user.username, 
			'id': user.id
		} 
		resp = make_response(json.dumps(rps), 200)
		return resp
	return json.dumps(rps)

@user.route("/logout", methods=['post'])
@login_required
def logout():
	session.pop('user_id')
	return make_response(json.dumps({'success': True}), 200)	

@user.route("/register", methods=['post'])
def create_user():
	params = request.get_json()
	user = User(username=params['username'])
	user.set_password(password=params['password'])
	erps = copy.deepcopy(error_response)
	db.session.add(user)
	try:
		db.session.commit()
	except Exception, e:  
		erps['error'] = repr(e)	
		return json.dumps(erps)

	erps['success'] = True	
	return json.dumps(erps)

