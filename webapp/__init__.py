#coding:utf-8
from flask import Flask, g, request, Response, session, make_response, abort
from functools import wraps
import json
import copy
from config import DevConfig
from ext import db, bcrypt
from models import User, Post
from random import randint
from controller.user import user
from controller.post import post
from controller.util import  error_response

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config_name)

	db.init_app(app)
	bcrypt.init_app(app)

	@app.before_request
	def before_request():
		print('hi request')
		if 'user_id' in session:
			g.userId = session['user_id']
			print('i coming == {} =='.format(session['user_id']))

	@app.errorhandler(404)
	def api_not_found(error):
		response404 = copy.deepcopy(error_response)
		response404['error'] = 'api 不存在'
		return Response(json.dumps(response404), 404, mimetype='application/json')

	@app.errorhandler(401)
	def api_not_authorized(error):
		response401 = copy.deepcopy(error_response)
		response401['error'] = 'api 未授权'
		return Response(json.dumps(response401), 401, mimetype='application/json')

	app.register_blueprint(user, url_prefix='/user')
	app.register_blueprint(post, url_prefix='/post')
					
	return app
