import os
import cv2
import numpy as np
import caffe
import urllib
import cPickle as pickle
from pymongo import MongoClient
from bson import ObjectId

# Set current path
path = os.path.dirname(os.path.abspath(__file__))