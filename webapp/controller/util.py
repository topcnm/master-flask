#coding:utf-8
from flask import abort, session
from functools import wraps

error_response = {
	'success': False,
	'result': None
}

def login_required(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		if 'user_id' in session:
			return func(*args, **kwargs)
		else:
			return abort(401)
	return wrapper

