#! /bin/bash

# Install all Python packages
sudo pip install --upgrade pip
sudo pip install numpy scipy matplotlib tables scikit-learn scikit-image multiprocess jupyter bloscpack pandas flask paramiko shapely boto3 opencv-python

# Install elastix
sudo apt-get update
sudo apt-get install -y elastix

# Install imagemagick
sudo apt-get install -y imagemagick

# Code repo
REPO_DIR="/shared/MouseBrainAtlas"
git clone https://github.com/mistycheney/MouseBrainAtlas.git $REPO_DIR
chown -R ubuntu $REPO_DIR

# Code repo for Xiang
REPO_DIR_XIANG="/shared/MouseBrainAtlasXiang"
git clone https://github.com/xiangjiph/MouseBrainAtlas.git $REPO_DIR_XIANG
chown -R ubuntu $REPO_DIR_XIANG

# Kakadu
wget http://kakadusoftware.com/wp-content/uploads/2014/06/KDU79_Demo_Apps_for_Linux-x86-64_170108.zip
unzip KDU79_Demo_Apps_for_Linux-x86-64_170108.zip -d /home/ubuntu/

# Ganglia
sudo apt-get install -y libapache2-mod-php7.0 php7.0-xml
sudo /etc/init.d/apache2 restart

# Setup Jupyter Notebook Server
CERTIFICATE_DIR="/home/ubuntu/jupyter_notebook_certificate"
JUPYTER_CONFIG_DIR="/home/ubuntu/.jupyter"

if [ ! -d "$CERTIFICATE_DIR" ]; then
    mkdir $CERTIFICATE_DIR
    openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout "$CERTIFICATE_DIR/mykey.key" -out "$CERTIFICATE_DIR/mycert.pem" -batch
    chown -R ubuntu $CERTIFICATE_DIR
fi

if [ ! -f "$JUPYTER_CONFIG_DIR/jupyter_notebook_config.py" ]; then
    # generate default config file
    #jupyter notebook --generate-config
    mkdir $JUPYTER_CONFIG_DIR

    # append notebook server settings
    cat <<EOF >> "$JUPYTER_CONFIG_DIR/jupyter_notebook_config.py"
# Set options for certfile, ip, password, and toggle off browser auto-opening
c.NotebookApp.certfile = u'$CERTIFICATE_DIR/mycert.pem'
c.NotebookApp.keyfile = u'$CERTIFICATE_DIR/mykey.key'
# Set ip to '*' to bind on all interfaces (ips) for the public server
c.NotebookApp.ip = '*'
c.NotebookApp.password = u'sha1:afce88b058a7:4c5afcebb62383f6f26404a08d6f5e89651709cb'
c.NotebookApp.open_browser = False

# It is a good idea to set a known, fixed port for server access
c.NotebookApp.port = 8888
c.NotebookApp.iopub_data_rate_limit = 10000000
EOF
    chown -R ubuntu $JUPYTER_CONFIG_DIR
fi

jupyter nbextension enable --py widgetsnbextension

# Install other utility programs
sudo apt install -y tree screen

# Install CellProfiler
git clone https://github.com/CellProfiler/CellProfiler.git /shared/CellProfiler
cd /shared/CellProfiler; git checkout 2.2.0
sudo apt-get install -y \
  build-essential \
  cython \
  libmysqlclient-dev \
  libhdf5-dev \
  libxml2-dev \
  libxslt1-dev \
  openjdk-8-jdk \
  python-dev \
    python-h5py \
    python-mysqldb \
    python-vigra \
  python-wxgtk3.0 \
  python-zmq
sudo pip install --editable .

echo """
export REPO_DIR=/shared/MouseBrainAtlas
alias sudosgeadmin=\"sudo -u sgeadmin -i\"
start_notebook() { jupyter notebook --notebook-dir \"$@\"; }
alias increase_ebs_size=\"sudo resize2fs /dev/xvdb\"
""" >> /home/ubuntu/.bashrc
