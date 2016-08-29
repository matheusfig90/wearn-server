import caffe
import cv2
import math
import numpy as np
import os
import random
import re
import cPickle as pickle
from pymongo import MongoClient
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.gridspec as gridspec

# Set current path
path = os.path.dirname(os.path.abspath(__file__))

# Set model and architecture
arch = path + '/../caffe/deploy.prototxt'
model = path + '/../caffe/bvlc_googlenet.caffemodel'

# Set image
image_file = path + '/adidas-preta-azul.jpg'

# Set caffe to run in CPU mode
caffe.set_mode_cpu()

# Create Caffe net
net = caffe.Net(arch, model, caffe.TEST)

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

# Get all layers names
layers = [key for key, val in net.blobs.iteritems()]

for layer in layers:
    print 'Saving', layer, '...'

    imgs = []
    
    # Get feature map
    for fmaps in net.blobs[layer].data:
        for fmap in fmaps:
            imgs += [fmap]
    ct = 0
    dim = int(math.ceil(math.sqrt(len(imgs))))
    gs = gridspec.GridSpec(dim, dim)
    gs.update(left=0.03, right=0.97, wspace=0.1, hspace=0.1)
    image_index = 0
    fig = plt.figure(ct)
    for i in range(dim):
        for j in range(dim):
            if image_index == len(imgs):
                break
            gr = plt.subplot(gs[i,j:j + 1])
            gr.axis("off")
            plt.imshow(imgs[image_index], interpolation="none")
            image_index += 1
    plt.savefig(path + '/feature-maps/adidas-preta-azul/' + re.sub('[^-a-zA-Z0-9_.() ]+', '', layer) + str(random.randint(1,1000)).zfill(4) + ".jpg")

print 'Done!'
