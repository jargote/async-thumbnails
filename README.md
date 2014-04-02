#Asynchronous-thumbnails

## Description

This project offers a django http server that generates thumbnails for image urls given in a specific JSON format.


    json = {
       "item1": {
            "title": "Image title",
            "description": "some description",
            "image_url": "/some/url/to/image"
        },
       "item2": {
            "title": "Image title2",
            "description": "some description2",
            "image_url": "/some/url/to/image2"
        },
     }

Asynchronous tasks are send to the Celery workers running. These download and generate the thumbnails of the image urls.

On completion these workers will trigger a notification to the push server running in NodeJS which means that the thumbnails are ready to be served.


## Architecture Overview

![Alt text](https://raw.githubusercontent.com/jargote/async-thumbnails/master/architecture_overview.jpg "Optional title")

##Prerequisites 

Make sure you have this libraries installed in your system or virtual env.

        1.  virtualenv
        2.  python-setuptools (pip)
        3.  nodejs
            *   express
            *   socket.io

##Setting up environment.

    >>  virtualenv async-thumbs
    >>  cd async-thumbs
    >>  source ./bin/activate
    
copy project folder to current folder so it looks like… /async-thumbs/thumbs/

    >>  cd thumbs
    >>  pip install -r requirements.txt

## Running the services


### Http Server (django)
    >>  ./manage.py runserver

### Push Server (nodejs)
    >>  cd push-server/
    >>  node server.js

### Celery Worker (run as many as you like to make it faster’)
    >>  cd ..
    >>  celery -A thumbs worker -l info


Visit http://localhost:8000 (default port)

Have fun!