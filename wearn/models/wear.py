# Dependencies
import caffe
import cPickle as pickle
import cv2
import numpy as np
import os
import random
import urllib

from scipy.spatial.distance import cosine, correlation
from wearn import app
from wearn.models.database import Database

# Get current path
path = os.path.dirname(os.path.abspath(__file__)) + '/../.env'

# Set caffe to run in GPU mode
caffe.set_mode_cpu()

"""
    Class to save and search wears.
"""
class Wear(object):

    # Set model and architecture to neural network
    arch  = os.path.dirname(os.path.abspath(__file__)) + '/../../caffe/deploy.prototxt'
    model = os.path.dirname(os.path.abspath(__file__)) + '/../../caffe/bvlc_googlenet.caffemodel'

    # Set caffe network
    net = caffe.Net(arch, model, caffe.TEST)

    # Set net layer
    layer = 'pool5/7x7_s1'

    """
        Search wears by image.

        Returns a prediction array
    """
    @staticmethod
    def search(image):
        # Set caffe network
        net = caffe.Net(Wear.arch, Wear.model, caffe.TEST)

        # Read image
        image_matrix = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], image))
        image_matrix = cv2.resize(image_matrix, (224, 224)) # Resize image to 224x224
        image_matrix = image_matrix[:, :, ::-1] # Convert BGR to RGB

        image_data = image_matrix.astype(np.float32)

        # Resize image
        net.blobs["data"].reshape(1, 3, 224, 224)

        image_data = image_data.transpose([2, 0, 1]) # Change channel

        net.blobs["data"].data[...] = image_data
        net.forward()

        # Get feature maps from image
        feature_maps = net.blobs[Wear.layer].data

        # Searching in database
        wears = Database.connect().wears.find({})

        # Set predictions to image
        predictions = []

        for wear in wears:
            # Get feature maps from wear
            wear_fm = pickle.loads(str(wear['feature_maps']))['_feature_maps']

            """ Calculating distances """
        
            # Euclidean distance
            euclidean_distance = np.sqrt(np.sum((feature_maps - wear_fm)**2.))

            # Cosine distance
            cosine_distance = cosine(feature_maps, wear_fm)

            # Correlation distance
            correlation_distance = correlation(feature_maps, wear_fm)

            predictions.append([str(wear['name']), str(wear['image']), str(wear['link']), euclidean_distance])

        return predictions

    """
        Save wear

        Returns new id
    """
    @staticmethod
    def save(args):
        if app.config['DEBUG'] == True:
            print 'Download image from ' + str(args['image'])
        
        # Download image
        image_file = '/tmp/' + str(random.randint(1,999999)) + '.jpg'
        urllib.urlretrieve(args['image'], image_file)

        # Read image and convert to matrix
        image_matrix = cv2.imread(image_file)
        image_matrix = cv2.resize(image_matrix, (224, 224)) # Resize image to 224x224
        image_matrix = image_matrix[:, :, ::-1] # Convert BGR to RGB

        image_data = image_matrix.astype(np.float32)

        # Resize image
        Wear.net.blobs["data"].reshape(1, 3, 224, 224)

        image_data = image_data.transpose([2, 0, 1])

        Wear.net.blobs["data"].data[...] = image_data
        Wear.net.forward()

        # Serialize feature maps to save in database
        feature_maps = pickle.dumps({ '_feature_maps': Wear.net.blobs[Wear.layer].data })

        return Database.connect().wears.insert_one({ 
            'name': args['name'],
            'image': args['image'],
            'price': float(args['price']),
            'link': args['link'],
            'feature_maps': feature_maps
        })