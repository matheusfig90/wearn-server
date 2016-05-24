# Dependencies
import os
import flask
import caffe

# Create application
app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp' # Settings upload path

@app.route('/')
def index():
    return 'Hello World!'

# Import routes
import wearn.routes
