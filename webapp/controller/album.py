#coding:utf-8
from flask import Blueprint, request, g
from random import randint
import time, os, sys, re
import imghdr
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
		img_type = re.search('\.[a-z]{2,}$', upload_file.filename).group()

		current_path = os.getcwd()
	 	new_folder_path = current_path + '/static/{}'.format(username)
		if not os.path.exists(new_folder_path):
			os.makedirs(new_folder_path)
 		upload_file.save('{}/{}.{}'.format(new_folder_path, t, img_type))
		
	return 'ttt'

# get the album list by user id
@album.route('/list')
def get_album_list():
	pass

# set the front-page for album
@album.route('/front-page')
def set_album_front_page():
	pass

# get the pic list by album id
@album.route('/pic/list')
def get_pic_list():
	pass

