---
layout: post
title: How to Host Multiple Python Apps on the Same Host With Nginx
date:   2018-01-21
categories: linux
---
## Configure NGINX as a reverse proxy

![NGINX](/static/img/nginx-logo.svg)

In this tutorial we assume that there are two python applications / sites running on ports 8000 and 8001 and we need to point example1.com to the application on port 8000 and example2.com to the application on port 8001.

First we need to make sure that the domains DNS is pointing to the external IP of our server.

Then we'll need to install nginx which will play the role of a proxy server that will forward the traffic from port 80 to the python application port depending on the origination domain.
	
	$ sudo apt-get install nginx
	
Once nginx is installed we need to create individual nginx site file for each site under `/etc/nginx/sites-available/`

/etc/nginx/sites-available/example1.com

<pre>
server {
	listen 80;
	server_name example1.com;
	access_log  /var/log/nginx/access.log;

	location / {
		proxy_pass http://127.0.0.1:8000;
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	}

}
</pre>

/etc/nginx/sites-available/example2.com

<pre>
server {
    listen 80;
    server_name example2.com;
    access_log  /var/log/nginx/access.log;

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

}
</pre>


To enable these sites for nginx, create a symlink from the files we just created to `/etc/nginx/sites-enabled/`.


	$ sudo ln -s /etc/nginx/sites-available/example1.com /etc/nginx/sites-enabled/example1.com
	$ sudo ln -s /etc/nginx/sites-available/example2.com /etc/nginx/sites-enabled/example2.com
	
After nginx is restarted to load the new sites we just created they should be resolving properly.
	
	$ sudo /etc/init.d/nginx restart
	

You can use this method to host more than two sites, just make sure you use the correct domain and port number in the nginx sites-available configuration file.

If you want to install SSL certificates for your domains you can look at this article -
[Install LetsEncrypt Certificate]({% post_url 2019-01-15-LetsEncrypt-Certificates %}) .
