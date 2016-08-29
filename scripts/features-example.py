import caffe
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.gridspec as gridspec
import math
import sys
import random
from timeit import default_timer as DT

class FeaturesExperiment():
    def __init__(self, arch, model, mode="gpu"):
        self.ct = 0
        self.arch = arch
        self.model = model
        if mode == "gpu":
            print "Mode: " + '\033[91m' + "GPU" + '\033[0m'
            caffe.set_mode_gpu()
        else:
            print "Mode: " + '\033[92m' + "CPU" + '\033[0m'
            caffe.set_mode_cpu()
    
    def setup(self):
        self.net = caffe.Net(self.arch, self.model, caffe.TEST)
    
    def print_layers_shape(self):
        print '\033[91m' + "Network Layers Shapes:" + '\033[0m'
        for key, blob in self.net.blobs.iteritems():
            print '\033[92m' + key + '\033[0m', "->", blob.data.shape
    
    def forward_image_file(self, image_path):        
        matrix = cv2.imread(image_path)
        # matrix = cv2.resize(matrix, (128, 128))
        matrix = matrix[:,:,::-1] # BGR2RGB
        self.forward_image(matrix.astype(np.float32))

    def forward_image(self, image_data):
        self.net.blobs["data"].reshape(1,3,227,227)
        image_data = image_data.transpose((2,0,1))
        plt.show()
        self.print_layers_shape()
        self.net.blobs["data"].data[...] = image_data
        self.net.forward()
        print "Image Mean:", np.mean(image_data)
        print "Output Shape", self.net.blobs["prob"].data.shape
        print "Scores:", -np.sort(-self.net.blobs["prob"].data.flatten())[:5]
        print "Top 5:", (-self.net.blobs["prob"].data.flatten()).argsort()[:5]

    def get_layers_name(self):
        return [key for key, val in self.net.blobs.iteritems()]

    def get_feature_maps(self, layer):
        imgs = []
        for fmaps in self.net.blobs[layer].data:
            print '\033[92m' + layer, fmaps.shape[0], "feature maps." + '\033[0m'
            for fmap in fmaps:
                imgs += [fmap]
        return imgs

    def plot_images(self, layer, imgs):
        dim = int(math.ceil(math.sqrt(len(imgs))))
        gs = gridspec.GridSpec(dim, dim)
        gs.update(left=0.03, right=0.97, wspace=0.1, hspace=0.1)
        image_index = 0
        self.fig = plt.figure(self.ct)
        self.ct += 1
        self.fig.canvas.mpl_connect("key_press_event",self.key_press)
        plt.gcf().canvas.set_window_title("Layer " + layer + ", " + str(len(imgs)) + " feature maps!")
        plt.get_current_fig_manager().window.showMaximized()
        for i in range(dim):
            for j in range(dim):
                if image_index == len(imgs):
                    break
                gr = plt.subplot(gs[i,j:j + 1])
                gr.axis("off")
                plt.imshow(imgs[image_index], interpolation="none")
                image_index += 1
        plt.savefig("img_outputs/" + layer + str(random.randint(1,1000)).zfill(4) + ".jpg")
        plt.show()

    def key_press(self, event):
        if event.key == 'x':
            plt.close(self.fig)

if __name__ == "__main__":
    arch = '/home/caffe/caffe/models/bvlc_reference_caffenet/deploy.prototxt'
    model = '/home/caffe/caffe/models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel'
    #arch = "/home/caffe/tmp/oficina/arquiteturas_oficina/lenet/deploy.prototxt"
    #model = "/home/caffe/Desktop/arquiteturas_oficina/lenet/snapshots/lenet_4_iter_10000.caffemodel"
    e = FeaturesExperiment(arch, model, "cpu")
    e.setup()    
    e.print_layers_shape()
    e.forward_image_file(sys.argv[1])

    for layer in e.get_layers_name():
        print "Show feature maps for layer", layer + "?[y/n/q]"
        input_char = raw_input()
        if input_char == "q":
            print "Quit!"
            sys.exit(0)
        if input_char == "y":
            imgs = e.get_feature_maps(layer)
            e.plot_images(layer, imgs)
