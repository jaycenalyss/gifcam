from flask import Flask
import os
app = Flask(__name__)

@app.route('/')
def index():
    images = ''
    for root, dirs, files in os.walk('.'):
    	for filename in [os.path.join(root,name) for name in files]:
        	if filename.endswith(".gif"):
            	images = images + '<a href="' + gifdirectory +  filename + '"><img src="gifs/'+filename + '" height=200 width=200 /></a>'
    if images != '':
        return images
    return '<h1> Sorry, no gifs exist </h1>'

@app.route('/gifs/<string:path>')
def send_gif(path):
    return '<img src="' + gifdirectory + path + '" />'
