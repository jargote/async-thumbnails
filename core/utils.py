import hashlib
import urllib
import urlparse
import os

from PIL import Image
from django.conf import settings


def _get_image_url_hash(url):
    return hashlib.sha1(url).hexdigest()


def _get_image_filename(mapper):
    return '{images_root}/{image_hash}.{file_extension}'.format(**mapper)


def _get_image_extension(path):
    path = path.split('/')  # /path/to/an/image.jpg
    image_name = path[-1:]  # ['path', 'to', 'an', 'image.jpg']
    if image_name:
        filename, extension = image_name[0].split('.')  # ['image', 'jpg']
        if extension in settings.ALLOWED_MIMETYPES:
            return extension
    return settings.DEFAULT_MIMETYPE


def retrieve_image_url(url):
    url_path = urlparse.urlsplit(url).path
    mapper = {'images_root': settings.IMAGES_ROOT,
              'image_hash': _get_image_url_hash(url),
              'file_extension': _get_image_extension(url_path)}
    filename = _get_image_filename(mapper)
    f = open(filename, 'wb')
    f.write(urllib.urlopen(url).read())
    f.close()

    _get_image_thumbnails(filename, mapper)


def _get_image_thumbnails(filename, mapper):
    outfile = os.path.join(mapper['images_root'], 'thumbs',
                           mapper['image_hash'] + '.thumb')
    try:
        im = Image.open(filename)
        im.thumbnail(settings.THUMB_SIZE, Image.ANTIALIAS)
        im.save(outfile, settings.DEFAULT_MIMETYPE)
    except IOError as e:
        print "cannot create thumbnail for '%s': %s" % (filename, e.message)