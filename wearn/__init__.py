# Dependencies
import os
import flask
import caffe

# Create application
app = flask.Flask(__name__)

# Load config settings
app.config.from_pyfile(os.path.dirname(os.path.abspath(__file__)) + '/../.env')

# Import routes
import wearn.routes
