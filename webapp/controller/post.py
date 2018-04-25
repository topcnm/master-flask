#coding:utf-8
from flask import Blueprint, request, Response, make_response
import json
import copy
from webapp.ext import db
from webapp.models import Post, User, Tag, Comment

post = Blueprint('post', __name__)

error_response = { 
	'success': False, 
	'result': None
 }

@post.route("/create", methods=['post'])
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

@post.route("/page", methods=['get'])
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

@post.route("/detail", methods=['get'])
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
				


