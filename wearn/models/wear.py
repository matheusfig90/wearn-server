# Dependencies
import caffe
import cPickle as pickle
import cv2
import numpy as np
import os
import random
import urllib
import matplotlib.image as mpimage

from PIL import Image
from scipy.spatial.distance import cosine, correlation
from wearn import app
from wearn.models.database import Database

# Get current path
current_path = os.path.dirname(os.path.abspath(__file__)) + '/../../'

# Set caffe to run in GPU mode, otherwise run in CPU mode
if app.config['GPU_MODE'] == True:
    caffe.set_mode_gpu()
else:
    caffe.set_mode_cpu()

"""
    Class to save and search wears.
"""
class Wear(object):

    # Set googlenet model and architecture
    googlenet_arch  = current_path + 'networks/bvlc_googlenet.deploy.prototxt'
    googlenet_model = current_path + 'networks/bvlc_googlenet.caffemodel'

    # Set fcn model and architecture
    fcn_arch  = current_path + 'networks/fcn-8s.deploy.prototxt'
    fcn_model = current_path + 'networks/fcn-8s.caffemodel'

    # Initialize googlenet network
    googlenet = caffe.Net(googlenet_arch, googlenet_model, caffe.TEST)

    # Initialize FCN network
    fcn = caffe.Net(fcn_arch, fcn_model, caffe.TEST)

    # Set googlenet layer
    googlenet_layer = 'pool5/7x7_s1'

    """
        Get feature maps from image

        Returns array
    """
    @staticmethod
    def get_feature_maps(image):
        # Read image and convert to array
        image_matrix = Image.open(image)
        image_matrix = np.array(image_matrix, dtype=np.float32)

        # Save original image in image_base variable
        image_base = image_matrix.copy().astype(np.uint8)

        # Prepare image matrix to FCN
        image_matrix = image_matrix[:, :, ::-1]
        image_matrix -= np.array((104.00698793, 116.66876762, 122.67891434))
        image_matrix = image_matrix.transpose((2, 0, 1))

        # Send image matrix to FCN
        Wear.fcn.blobs['data'].reshape(1, *image_matrix.shape)
        Wear.fcn.blobs["data"].data[...] = image_matrix

        # Forward in network
        Wear.fcn.forward()

        # Get output by FCN
        output = Wear.fcn.blobs['score'].data[0].argmax(axis=0)

        # Normalize output
        output[output != 0] = 1
        output[output == 0] = 0

        # Merge image to remove background
        image_matrix = image_base * np.asarray(np.dstack((output, output, output)))
        image_matrix = np.asarray(image_matrix, dtype=np.float32)
        image_matrix = cv2.resize(image_matrix, (224, 224))
        image_matrix = image_matrix.transpose([2, 0, 1])

        # Resize image
        Wear.googlenet.blobs["data"].reshape(1, 3, 224, 224)

        # Send image to googlenet network
        Wear.googlenet.blobs["data"].data[...] = image_matrix

        # Forward in network
        Wear.googlenet.forward()

        return Wear.googlenet.blobs[Wear.googlenet_layer].data

    """
        Search wears by image.

        Returns a prediction array
    """
    @staticmethod
    def search(image):
        # Get feature maps from image
        feature_maps = Wear.get_feature_maps(image)

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

            predictions.append([str(wear['image']), str(wear['link']), euclidean_distance])

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

        # Get searialize feature maps
        feature_maps = pickle.dumps({ '_feature_maps': Wear.get_feature_maps(image_file) })

        return Database.connect().wears.insert_one({ 
            'name': args['name'],
            'image': args['image'],
            'price': float(args['price']),
            'link': args['link'],
            'feature_maps': feature_maps
        })
