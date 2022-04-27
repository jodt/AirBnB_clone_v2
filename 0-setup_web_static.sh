#!/usr/bin/env bash
#script that sets up your web servers for the deployment of web_static
apt-get -y update
apt-get -y install nginx
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/ 
echo "hello world" > /data/web_static/releases/test/index.html
ln -s -f /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu: /data/
sed -i '56 i location /hbnb_static {\n\t alias /data/web_static/current;/\n}' /etc/nginx/sites-enabled/default
service nginx restart