---
layout: post
title: How to translate a Flask site with Babel
description: "Translate a Flask website with Flask-Babel: configure locales, tag strings in Python and Jinja2 templates, then extract, translate and compile catalogs."
date:   2018-02-24
categories: python
---

![Flask-Babel workflow: tag strings, pybabel extract, init, translate, compile](/static/img/flask-babel-header.svg){: width="1000" height="360"}

This article will show you how to translate your Fask site using the python module Babel on a Debian based system running python 3.

## Install Flask-Babel

First you need to install the python module [Flask-Babel](https://pythonhosted.org/Flask-Babel/).

```
$ sudo pip install Flask-Babel
```

## Configure Flask-Babel and hook it to your site
Once Babel is installed we'll need to configure it.

Create a file named ''babel.cfg'' in the root of your flask project and put the code below in it.

```
[python: **.py]
[jinja2: **.html]
extensions=jinja2.ext.autoescape,jinja2.ext.with_
```

Now we need to hook babel to our flask application as shown below:

```
from flask import Flask, [...]
from flask.ext.babel import Babel, gettext
app = Flask(__name__)
babel = Babel(app)
```

Also we need to tell Babel what languages we need to support, put the code below in your application.
In this example, we add two locales, english (‘en’) and bulgarian (‘bg’).
```
# add to you main app code
LANGUAGES = {
    'en': 'English',
    'bg': 'Bulgarian'
}
```

Finally we need to make our code select the best matching locale, based on the Accept-Language header from the incoming request.
```
# add to you main app code
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())
```

##Tagging Strings for Translation

Once you installed and configured Flask-Babel it’s time to tag all the Strings you want to translate. In a typical Flask app, there will be two types of Strings that require translating. One being hard-coded Strings in your .py files and the other being Strings in your .html Jinja2 templates.

### Tagging Strings in py files:

```
title = 'My home page title'
print('Text for tanslation')

```
becomes
```
title = gettext('My home page title')
print(gettext('Text for tanslation'))

```


### Tagging Strings in  Jinja2 templates:

```
<p class="lead">Movies found today.</p>
<input type="submit" value="Search"/>
```
becomes
```
<p class="lead"> {{ gettext('Movies found today.') }}</p>
<input type="submit" value="{{ gettext('Search') }}"/>

```

You can use _() as a shortcut for gettext().

## Building Locales

Once we have tagged all the string in our code and templates, its time to build a catalog for the Locales we want to create.  Run:
```
$ pybabel extract -F babel.cfg -o messages.pot --input-dirs=.
```

This checks all files specified in babel.cfg and searches through them to find tagged strings and outputs them to messages.pot.
After all the translated strings are indexed its time to initialize our locale:

```
$ pybabel init -i messages.pot -d translations -l bg
```
The example above initializes the Bulgarian locale and creates the files we need to translate.
Open ``translations/bg/LC_MESSAGES/messages.po`` with you favorite text editor and translate the msgstr values for all the strings you have tagged. 

The final step to get your site translated is to compile the ``messages.po`` file, to do so run the command below:

```
$ pybabel compile -d translations
```

## Updating locales

After a while you'll add new content to your site and there will be new strings for translation.
Run again this command to extract the new strings:
```
$ pybabel extract -F babel.cfg -o messages.pot --input-dirs=.
```
Then run pybabel update to update your locale file ``messages.po``

```
$ pybabel update -i messages.pot -d translations
```
Translate the new strings and compile your locale:

```
$ pybabel compile -d translations
```
