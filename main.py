#coding:utf-8
from flask import Flask, g, request, Response, session, make_response, abort
from functools import wraps
import json
import copy
from config import DevConfig
from ext import db, bcrypt
from models import User, Post
from random import randint

app = Flask(__name__)
app.config.from_object(DevConfig)
db.init_app(app)
bcrypt.init_app(app)

@app.before_request
def before_request():
	if 'user_id' in session:
		g.userId = session['user_id']
		print('i coming == {} =='.format(session['user_id']))

error_response = { 
	'success': False, 
	'result': None
 }
	
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

# 登录要求
def login_required(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		if 'user_id' in session:
			return func(*args, **kwargs)
		else:
			return abort(401)
	return wrapper

@app.route("/blog/login", methods=['post'])
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

@app.route("/blog/logout", methods=['post'])
@login_required
def logout():
	session.pop('user_id')
	return make_response(json.dumps({'success': True}), 200)	

@app.route("/blog/register", methods=['post'])
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

@app.route("/blog/create", methods=['post'])
@login_required
def post_article():
	params = request.get_json()
	print params
	post = Post(title=params['title'], text=params['text'], publish_able=params['publishable'], tag_id=params['tagId'])
	post.user_id = g.userId
	erps = copy.deepcopy(error_response)

	db.session.add(post)
	try:
                db.session.commit()
        except:  
                erps['error'] = '新建错误'
                return json.dumps(erps)

        erps['success'] = True
        return json.dumps(erps)

@app.route("/blog/search/<pageNo>")
@login_required
def get_user(pageNo):
	return '验证页面（必须登录）第（{}）页 '.format(pageNo)

@app.route("/blog/page", methods=['get'])
def get_blog_page():
	params = request.args
	keyword = params['keyword']
	tag_id = params['tagId']
	page_no = int(params['pageNo'])
	page_size = int(params['pageSize'])
	start_item_no = (page_no - 1) * page_size + 1
	end_item_no = page_no * page_size
	print(start_item_no, end_item_no)
	post_page = Post.query.filter(
		Post.publish_able == 1, 
		Post.tag_id == tag_id,
		keyword and Post.title.like('%{}%'.format(keyword))
	).paginate(start_item_no, end_item_no)
	total = post_page.pages
	posts = []
	for i in post_page.items:
		temp = {}
		posts.append({
			'id': i.id,
			'title': i.title,
			'tagId': i.tag_id,
			'tagName': i.tag.remark,
			'publishDate':i.publish_date.strftime('%Y-%m-%d'),
			'authorName': i.user.username,	
		})	

	resp = copy.deepcopy(error_response)
	resp['success'] = True
	resp['result'] = {
		'total': total,
		'list' : posts
	}
	return Response(json.dumps(resp), 200, mimetype='application/json')

@app.route("/blog/detail", methods=['get'])
def get_post_detail():
	postId = request.args.get('postId')
	post = Post.query.filter(Post.id == postId).first()
	reps = copy.deepcopy(error_response)
	if post:
		result = {
			'title': post.title,
			'text' : post.text,
			'tagName': post.tag.remark,
			'publishDate':post.publish_date.strftime('%Y-%m-%d'),
			'authorName': post.user.username,
		}
		reps['success'] = True
		reps['result']  = result
		return Response(json.dumps(reps), 200, mimetype='application/json')
		
	return Response(json.dumps(reps), 402, mimetype='application/json')	
				
	





if __name__ == '__main__':
	app.run()
