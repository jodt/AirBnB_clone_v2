#!/usr/bin/env bash
#script that sets up your web servers for the deployment of web_static
sudo apt-get -y update
sudo apt-get -y install nginx
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/ 
sudo echo "hello world" > /data/web_static/releases/test/index.html
sudo ln -s -f /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu: /data/
sudo sed -i '56 i location /hbnb_static {\n\t alias /data/web_static/current/\n}' /etc/nginx/sites-enabled/default
sudo service nginx restart