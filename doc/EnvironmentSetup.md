
# Software installation

### Python packages 

First install pip:
`sudo apt-get install python-pip`

It is recommended to install and use virtualenv ([guide](http://exponential.io/blog/2015/02/10/install-virtualenv-and-virtualenvwrapper-on-ubuntu)).

To install required Python packages, 
`pip install -r requirements.txt`

[`requirements.txt`](https://github.com/mistycheney/MouseBrainAtlas/blob/master/requirements.txt) specifies the names and versions of all packages.

### Jupyter (iPython)
`pip install jupyter`

### PyQt4 (required for annotation GUI)
`sudo apt-get install python-qt4`

### Others


# Login into servers

If using AWS, 
- On your local machine, run:
`cfncluster --config <config> create <clusterName>`.
Wait until the cluster creation finishes to see the master node IP, or log onto AWS EC2 console to get the IP.
- Log in the master node. `ssh -i /home/yuncong/aws/YuncongKey.pem ubuntu@<server_ip>`.

If using the lab workstation,
- Log in workstation, `ssh <workstaton_ip>`.

# Configuring iPython notebook server

Follow the steps in [Running a public notebook server](http://jupyter-notebook.readthedocs.io/en/stable/public_server.html).

Additionally, in `.jupyter/jupyter_notebook_config.py` set `c.NotebookApp.ip = '*'`.

# Launching iPython notebook server

The following steps work the same for both AWS and the lab workstation.
- Run `screen` to open a screen session (so the processes continue even if the terminal/SSH connection is closed)
- Run `REPO_DIR=<project_repo_dir> jupyter notebook <project_repo_dir> &` to start a Jupyter notebook in the background.
- Run `screen -d` to detach the screen session.

Then on your local machine,
- Open a browser and go to `https//<server_ip>:8888` (assuming the Jupyter notebook uses port 8888; try `http` instead of `https` if this failed). You can now access the notebook.

# Other commands
- `screen -r <session_id>` to resume the screen session.
- `fg` to bring the Jupyter notebook process to foreground.
- `bg` to put a process into background.

If tab and arrow keys are not working, you are using sh rather than bash. Do the following:
https://askubuntu.com/questions/163802/backspace-tab-del-and-arrow-keys-not-working-in-terminal-using-ssh
