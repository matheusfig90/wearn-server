# Installing a Caffe Framework
cd ~
sudo apt-get -y install build-essential linux-headers-`uname -r` curl
curl -O "http://developer.download.nvidia.com/compute/cuda/6_5/rel/installers/cuda_6.5.14_linux_64.run"
sudo chmod +x cuda_6.5.14_linux_64.run
sudo ./cuda_6.5.14_linux_64.run --override --kernel-source-path=/usr/src/linux-headers-`uname -r`/
echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64:/usr/local/lib' >> ~/.bashrc
sudo apt-get install -y libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libboost-all-dev libhdf5-serial-dev protobuf-compiler gfortran libjpeg62 libfreeimage-dev libatlas-base-dev git libgoogle-glog-dev libbz2-dev libxml2-dev libxslt-dev libffi-dev libssl-dev libgflags-dev liblmdb-dev python-yaml
sudo easy_install pillow
cd ~
git clone https://github.com/BVLC/caffe.git
cd caffe
cat python/requirements.txt | xargs -L 1 sudo pip install
sudo ln -s /usr/include/python2.7/ /usr/local/include/python2.7
sudo ln -s /usr/local/lib/python2.7/dist-packages/numpy/core/include/numpy/ /usr/local/include/python2.7/numpy
cp /var/www/wearn/caffe/Makefile.config .
make pycaffe -j8
make all -j8
make test -j8
echo 'export PATH="/home/vagrant/caffe/build/tools:$PATH"' >> ~/.bashrc
echo 'export PYTHONPATH=/home/vagrant/caffe/python' >> ~/.bashrc
echo 'export LC_ALL=en_US.UTF-8'>> ~/.bashrc
echo 'export LANG=en_US.UTF-8'>> ~/.bashrc
source ~/.bashrc
