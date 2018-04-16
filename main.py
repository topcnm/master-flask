#coding:utf-8
from flask import Flask
from config import DevConfig
from ext import db

app = Flask(__name__)
app.config.from_object(DevConfig)
db.init_app(app)

@app.route("/")
def home():
	return 'Hello World'

@app.route("/search/<pageNo>")
def get_user(pageNo):
	return '12 {}'.format(pageNo)

if __name__ == '__main__':
	app.run()
