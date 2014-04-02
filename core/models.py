import hashlib
import urllib
import os

from PIL import Image

from django.conf import settings
from django.db import models


class ImageUrl(models.Model):
    """This model represents an ImageUrl instance."""

    title = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.URLField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['image_url']

    def __init__(self, *args, **kwargs):
        super(ImageUrl, self).__init__(*args, **kwargs)

        self._mapper = {}
        self._filename = ''
        self._url_hash = ''

    @property
    def image_filename(self):
        """Generates a file name for related to the image url."""

        if not self._filename:
            self._filename = (
                '{images_root}/{image_hash}{file_extension}'.format(
                    **self.filename_mapper))

        return self._filename

    @property
    def filename_mapper(self):
        """Generates an object mapping to create an image filename."""

        if not self._mapper:
            self._mapper = {
                'images_root': settings.IMAGES_ROOT,
                'image_hash': self.image_url_hash,
                'file_extension': os.path.splitext(self.image_url)[1]}

        return self._mapper

    @property
    def image_url_hash(self):
        """Generates a Sha1.hexdigest using image_url attribute."""

        if not self._url_hash:
            self._url_hash = hashlib.sha1(self.image_url).hexdigest()

        return self._url_hash

    @property
    def thumbnails_urls(self):
        """Generates a dictionary pointing to this image's thumbnail files."""

        return {'thumb': settings.THUMBS_URL + self.thumb_filename(),
                'sqthumb': settings.THUMBS_URL + self.thumb_filename(1)}

    def retrieve_image_url(self):
        """Downloads and stores an image from the web."""
        # Making sure that only image files are downloaded and not any other
        # MIME types
        curr_file_extension = self.filename_mapper['file_extension']
        if curr_file_extension not in settings.ALLOWED_MIMETYPES:
            raise TypeError(
                'image_url should point to an image file type (%s):%s (current)'
                % (settings.ALLOWED_MIMETYPES, curr_file_extension))

        # Download and save image file from the web.
        f = open(self.image_filename, 'wb')
        f.write(urllib.urlopen(self.image_url).read())
        f.close()

    def thumb_filename(self, thumb_type=0):
        """Generates filenames form image file thumbnails

        thumb_type:
            0 - Thumbnail with aspect ration conservation.
            1 - Square thumbnail not conserving aspect ratio.
        """

        if thumb_type == 1:
             suffix = '.sqthumb.jpg'

        elif thumb_type == 0:
            suffix = '.thumb.jpg'

        return self.image_url_hash + suffix

    def generate_image_thumbnails(self):
        """Generates image thumbnails for downloaded image."""

        # Thumbnail conserving aspect ratio.
        thumb = Image.open(self.image_filename)
        thumb.thumbnail(settings.THUMB_SIZE, Image.ANTIALIAS)
        thumb.save(os.path.join(settings.THUMBS_ROOT, self.thumb_filename()),
                   settings.DEFAULT_MIMETYPE)

        sq_thumb = thumb.resize(settings.THUMB_SIZE, Image.ANTIALIAS)
        sq_thumb.save(os.path.join(settings.THUMBS_ROOT,
                                   self.thumb_filename(1)),
                      settings.DEFAULT_MIMETYPE)

