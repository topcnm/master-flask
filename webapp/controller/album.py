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

# get the album list by user id
@album.route('/list')
def get_album_list():
	pass

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

