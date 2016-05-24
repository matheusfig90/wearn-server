import sys
sys.path.insert(0, '/var/www/wearn')
sys.path.insert(0, '/usr/include/python2.7')
sys.path.insert(0, '/usr/local/lib/python2.7/dist-packages/numpy/core/include')
sys.path.insert(0, '/home/vagrant/caffe/python') # Import caffe modules

from wearn import app as application
