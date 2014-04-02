from __future__ import absolute_import

import logging
import simplejson as json
import urllib
import urllib2

from celery import shared_task
from core import models
from django.conf import settings


@shared_task
def create_image(session_id, **kwargs):
    """This tasks first creates a new ImageUrl instance then it attempts to
    download the image file from the given image_url attribute, upon success
    thumbnails are generated for this image file and finally an new asynchronous
    task to notify client is triggered.
    """

    try:
        # Creating ImageUrl instance.
        image_obj = models.ImageUrl(**kwargs)
        # Attempting to download and save image from url.
        image_obj.retrieve_image_url()
        # Generating downloaded image thumbnails.
        image_obj.generate_image_thumbnails()
        # Notify client associated to this session_id.
        notify_client.apply_async(args=[session_id, image_obj])
    except (IOError, TypeError) as e:
        # Log error message on fail.
        logging.error(e)
    else:
        # On success save ImageUrl instance.
        image_obj.save()

@shared_task
def notify_client(session_id, image_obj):
    try:
        # Push server host url.
        url = settings.PUSH_SERVER + '/' + session_id + '/'

        # Notification data.
        params = urllib.urlencode(
            {'thumbs': json.dumps(image_obj.thumbnails_urls)}
        )

        # Notify push server.
        response = urllib2.urlopen(url, params).read()

        return response
    except IOError as e:
        # Log error message on fail.
        logging.error(e)
