from flask import Flask
import os
app = Flask(__name__)

gifdirectory = '/home/pi/gifcam/gifs/'

@app.route('/')
def index():
    images = ''
    for filename in os.listdir(gifdirectory):
        if filename.endswith(".gif"):
            images = images + '<a href="gifs/' + filename + '"><img src="gifs/'+filename + '" height=200 width=200 /></a>'
    if images != '':
        return images
    return '<h1> Sorry, no gifs exist </h1>'

@app.route('/gifs/<path:path>')
def send_gif(path):
    return send_from_directory(gifdirectory, path)
