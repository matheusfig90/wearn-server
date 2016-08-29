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

# Set model and architecture
arch = path + '/../caffe/deploy.prototxt'
model = path + '/../caffe/bvlc_googlenet.caffemodel'

# Set caffe to run in CPU mode
caffe.set_mode_cpu()

# Create Caffe net
net = caffe.Net(arch, model, caffe.TEST)

# Show pool5/7x7_s1 layer
layer = 'pool5/7x7_s1'

# Connect into database
mongoClient = MongoClient('mongodb://localhost:27017/')
db = mongoClient.wearn

# Download all images
for clothing in db.clothings.find({ 'feature_maps': { '$exists': False } }):
    print 'Downloading image from: ' + str(clothing['image'])

    # Set image file
    image_file = '/tmp/wearn/' + str(clothing['_id']) + '.jpg'
    
    # Save image
    urllib.urlretrieve(clothing['image'], image_file)

    # Get image
    image_matrix = cv2.imread(image_file)
    image_matrix = cv2.resize(image_matrix, (224, 224)) # Resize image to 224x224
    image_matrix = image_matrix[:, :, ::-1] # Convert BGR to RGB

    image_data = image_matrix.astype(np.float32)

    # Resize image
    net.blobs["data"].reshape(1, 3, 224, 224)

    image_data = image_data.transpose([2, 0, 1])

    net.blobs["data"].data[...] = image_data
    net.forward()

    # Save feature maps in database
    clothing['feature_maps'] = pickle.dumps({ 'wearn': net.blobs[layer].data })

    db.clothings.update({ 
        '_id': ObjectId(clothing['_id']) 
    }, {
        'name': clothing['name'],
        'image': clothing['image'],
        'price': float(clothing['price']),
        'link': clothing['link'],
        'feature_maps': clothing['feature_maps'] 
    }, upsert=False)

print 'Done!'
