---
layout: post
title: "How to Create a Static Site with Python (Pelican) and Host It for Free"
description: "Create a static website with Pelican, the Python static site generator, preview it locally and host it for free on GitHub Pages with a custom domain."
seo_title: "Build a Static Site with Pelican and Host It Free on GitHub Pages"
date:   2018-03-08
categories: python
---
In this articel I'll show you how to create a static html site with Pelican and host it for free at [GitHub Pages](https://pages.github.com/){:target="_blank"}.
-------------------------

[Pelican](https://github.com/getpelican/pelican){:target="_blank"} is a static site generator, written in Python, that requires no database or server-side logic.
![Pelican](/static/img/python_pelican.png){: width="298" height="300"}

### Installing Pelican

The easiest way to install Pelican is using ```pip```, use the command below to install it along with the Markdown module:

```
$ sudo pip install pelican Markdown
```

### Initialize your site

Once Pelican has been installed, you can create a skeleton project via the ```pelican-quickstart``` command, which begins by asking some questions about your site:

```
$ pelican-quickstart
```

Once you answer all questions Pelican will create the files and folders shown below:

```
yourproject/
├── content
│   ├── (pages)          # These folders are not auto-created
│   ├── (posts) 
│   └── (images)
├── output
├── develop_server.sh
├── fabfile.py
├── Makefile
├── pelicanconf.py       # Main settings file
└── publishconf.py       # Settings to use when ready to publish
```

Your site content should be placed in the content folder. If you plan to create a blog, you'll need to create a folder named ```posts``` in the ```content``` folder, if you need just static pages that are not chronological create a folder named ```pages```.


The images for your site or blog should be located in the `content/images` folder.

You also need to tell Pelican that this folder holds your static content and images by adding the line below to 'pelicanconf.py' :

```
STATIC_PATHS = ['images']
```
You can have more than one folder for static content and you can also pick another location.

### Building your content

To create a new page or blog post you need to create a file in the ```pages``` or ```posts``` folder.
This file needs to be ending in .md, .markdown, .mkd, or .mdown and contain text formated with markdown syntax. 

Your file may contain the following meta-data (not all values are mandatory)

```html
Title: My post title
Date: 2018-02-03 11:21
Modified: 2018-02-05 17:30
Category: Python
Tags: pelican, publishing
Slug: my-blog-post
Authors: John Smith, Hristo Jelev
Summary: Short version for index and feeds

This is the content of my first blog post.
```

To add images to your content use the markdown below:

```
![Alt text](images/filename.jpg)
```

Add link with target="_blank":

```
[link](url){:target="_blank"}
```
If you are not familiar with markdown syntax look at [markdown cheat sheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet){:target="_blank"}

Once you create all the pages and articles its time to generate your site html.

### Generating your site HTML

To generate your site, go to your project root folder and run the command below:

```
$ pelican content
```
You can also use:

```
$ pelican -r
```
This command will regenerate your site each time a change is detected.

When the generation is complete all the files (html, images, css and maybe others) for your new site will be located in the `output` folder.

### Preview your site

Its useful to view your site before uploading it to your hosting. To run a local web server use one of the commands below.

For Python 2, run:

```
$ cd output
$ python -m SimpleHTTPServer
```

For Python 3, run:

```
$ cd output
$ python -m http.server
```

Once you start the web server you can preview your site at `http://localhost:8000/`.

### Hosting

One of the best free places to host your static site for free is [Github Pages](https://pages.github.com/){:target="_blank"}

![Github Pages](/static/img/github_logo.png){: width="573" height="248"}

On github pages you'll find detailed instructions how to upload your site with git.
If you don't have git installed you can install it with:

```
$ sudo apt-get install git
```

Once your site is uploaded to github pages its url will look like this `https://username.github.io`.


You can change this by adding a custom domain to your github repository.
If you don't have a domain name you can get one for free from http://www.dot.tk - they offer five domain extension for free (.tk, .ga, .ml, .cf and .gq).

First add your domain name to your new github repository by following [these](https://help.github.com/articles/adding-or-removing-a-custom-domain-for-your-github-pages-site/){:target="_blank"} instructions.

Then point your custom domain to the following IP addresses:
```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

[Here](https://help.github.com/articles/setting-up-an-apex-domain/){:target="_blank"} are other ways to point your domain to github pages.
   