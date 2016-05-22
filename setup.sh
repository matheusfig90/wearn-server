# Exporting envorinment variables
echo 'export LC_ALL=en_US.UTF-8'>> ~/.bashrc
echo 'export LANG=en_US.UTF-8'>> ~/.bashrc

# Update all softwares installeds
sudo apt-get -y update

# Installing basic modules
sudo apt-get -y install vim apache2 libapache2-mod-wsgi python-pip

# Installing all requirements projects
sudo pip install -r /var/www/wearn/requirements.txt

# Installing MongoDB
sudo apt-get -y mongodb

# Create site in apache
cd /etc/apache2
sudo a2dissite 000-default
sudo cp /var/www/wearn/wearn.conf sites-available/
sudo a2ensite wearn.conf
sudo service apache2 reload

# For install caffe framework
sudo chmod +x /var/www/wearn/caffe/setup.sh
