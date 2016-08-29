# Dependencies
import os
import cv2
import caffe
import numpy as np
import cPickle as pickle
from wearn import app, flask
from flask import request, jsonify
from pymongo import MongoClient
from scipy.spatial.distance import cosine, correlation

# Set current path
path = os.path.dirname(os.path.abspath(__file__))

# Set caffe to run in CPU mode
caffe.set_mode_cpu()

# Connect into database
mongoClient = MongoClient(app.config['DB_HOST'])
db = mongoClient.wearn

# @app.route('/api/v1/search', methods=['GET'])
# def search():

#     # Set model and architecture
#     arch = '/var/www/wearn/caffe/deploy.prototxt'
#     model = '/var/www/wearn/caffe/bvlc_googlenet.caffemodel'

#     # Create Caffe net oject
#     net = caffe.Net(arch, model, caffe.TEST)

#     # Get file
#     file = request.files['file']
#     file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

#     # Read image
#     image_matrix = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
#     image_matrix = cv2.resize(image_matrix, (224, 224)) # Resize image to 224x224
#     image_matrix = image_matrix[:, :, ::-1] # Convert BGR to RGB

#     image_data = image_matrix.astype(np.float32)

#     # Resize image
#     net.blobs["data"].reshape(1, 3, 224, 224)

#     image_data = image_data.transpose([2, 0, 1]) # Change channel

#     net.blobs["data"].data[...] = image_data
#     net.forward()

#     # Get feature maps from file
#     feature_maps = net.blobs['pool5/7x7_s1'].data

#     # Searching in database
#     predictions = []
#     for clothing in db.clothings.find({}):
#         # Get feature maps from clothing
#         clothing_fm = pickle.loads(str(clothing['feature_maps']))['wearn']

#         """ Calculating distances """
        
#         # Euclidean distance
#         euclidean_distance = np.sqrt(np.sum((feature_maps - clothing_fm)**2.))

#         # Cosine distance
#         cosine_distance = cosine(feature_maps, clothing_fm)

#         # Correlation distance
#         correlation_distance = correlation(feature_maps, clothing_fm)

#         predictions.append([
#             str(clothing['name']),
#             str(clothing['image']),
#             str(clothing['link']),
#             euclidean_distance,
#             cosine_distance,
#             correlation_distance
#         ])

#     # Show best results by euclidean distance
#     predictions_by_euclidean = sorted(predictions, key=lambda x: x[3])[:10]

#     # Show best results by cosine distance
#     predictions_by_cosine = sorted(predictions, key=lambda x: x[4])[:10]

#     # Show best results by correlation distance
#     predictions_by_correlation = sorted(predictions, key=lambda x: x[5])[:10])

#     return jsonify(
#         predictions_by_correlation=predictions_by_correlation,
#         predictions_by_euclidean=predictions_by_euclidean,
#         predictions_by_cosine=predictions_by_cosine
#     )
