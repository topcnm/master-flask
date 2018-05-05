#coding:utf-8
from flask import Blueprint, request, g
from random import randint
from webapp.ext import db
from webapp.models import Album, Picture
import time, os, sys, re
import imghdr
import json
import copy
from util import login_required, error_response

album = Blueprint('album', __name__)

# upload the pic file
@album.route('/upload', methods=['post'])
@login_required
def receive_album():
	# get fname 
	upload_file = request.files.get("files")
	if upload_file:
		t = time.strftime('%Y%m%d%H%M%S')
		username = g.username
		userId = g.userId
		img_type = re.search('\.[a-z]{2,}$', upload_file.filename).group()

		current_path = os.getcwd()
	 	new_folder_path = current_path + '/static'
		if not os.path.exists(new_folder_path):
			os.makedirs(new_folder_path)
		new_file_path = '{}/{}{}'.format(new_folder_path, t, img_type)
		new_ref_file_path = '/static/{}{}'.format(t, img_type)
 		upload_file.save(new_file_path)
		
		# insert 
		pic = Picture(remark='', full_link=new_ref_file_path, user_id=userId)
		db.session.add(pic)
		db.session.commit()

		reps = copy.deepcopy(error_response)
		reps['success'] = True
		reps['result'] = {
			'fileName': upload_file.filename,
			'filePath': new_ref_file_path,
		} 	
		return json.dumps(reps)
	return json.dumps(error_response)

@album.route('/create', methods=['post'])
@login_required
def create_album():
	params = request.get_json()
	userId = g.userId
	title = params.get('title')
	remark = params.get('remark')
	publish_able = params.get('publishAble')
	album = Album(user_id=userId, title=title, remark=remark, publish_able=publish_able)	
	db.session.add(album)
	try:
		db.session.commit()
		reps = copy.deepcopy(error_response)
		reps['success'] = True
		return json.dumps(reps)
	except Exception, e :		
		print(e)
	        return json.dumps(error_response)

@album.route('/delete', methods=['post'])
@login_required
def delete_album():
	params = request.get_json()
	userId = g.userId
	album_id = params.get('albumId')
	album = Album.query.filter(Album.id == album_id).first()
	if album.user_id == userId:
		db.session.delete(album)
		db.session.commit()
		reps = copy.deepcopy(error_response)
		reps['success'] = True
	else:
    		reps = copy.deepcopy(error_response)
		reps['msg']= 'No right to delete' 	
		
	return json.dumps(reps)


@album.route('/pic/belong', methods=['post'])
@login_required
def set_pic_belong():
        params = request.get_json()
	album_Id = params.get('albumId')
	pic_id_list = params.get('piclist').split(",")
	user_id = g.userId
	print(999, params)	
	return 'finish'


# get the album list by user id
@album.route('/list', methods=['get'])
def get_album_list():
	params = request.args
	userId = params.get('userId')
	
	album_list = Album.query.filter(
		Album.user_id == userId
	)
	albums = []
	for album in album_list:
		albums.append({
			'id': album.id,
			'title': album.title,
			'front': album.front,
			'remark': album.remark,
			'userId': album.user_id,
		})
        resp = copy.deepcopy(error_response)
	resp['success'] = True
	resp['result'] = {
		'total': len(albums),
		'list': albums
	}
	return json.dumps(resp)


# set the front-page for album
@album.route('/front-page')
def set_album_front_page():
	pass

# get the pic list by album id, if no album getted , return all picture
@album.route('/pic/list', methods=['get'])
def get_pic_list():
        params = request.args
	# no album meaning is "get all uncategory pics"
	albumId = params.get('albumId') or None
	userId = params.get('userId')
	print(albumId, userId)
	pic_list = Picture.query.filter(
		Picture.album_id == albumId,
		Picture.user_id == userId
	)
	pics = []
	for pic in pic_list:
		pics.append({
			'url': pic.full_link,
			'id': pic.id,
			'remark': pic.remark
		})
        resp = copy.deepcopy(error_response)
	resp['success'] = True
	resp['result'] = {
		'total': len(pics),
		'list': pics
	}
	return json.dumps(resp)

