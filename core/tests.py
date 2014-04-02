import os

from core.models import ImageUrl
from django.conf import settings
from django.test import TestCase


class ImageUrlTest(TestCase):

    def setUp(self):
        """Setting up test suite environment variables."""

        self.dummy_image = ImageUrl.objects.create(
            title='Dummy Title', description='Dummy Desc',
            image_url='https://www.google.com.au/images/srpr/logo11w.png')

    def tearDown(self):
        """Cleaning test environment on exit."""

        def remove_thumb(thumb_type):
            thumb = os.path.join(settings.THUMBS_ROOT,
                                 self.dummy_image.thumb_filename(thumb_type))
            if os.path.exists(thumb):
                os.remove(thumb)

        # Removing downloaded test image.
        if os.path.exists(self.dummy_image.image_filename):
            os.remove(self.dummy_image.image_filename)

        # Removing downloaded test image thumbnails.
        remove_thumb(0)
        remove_thumb(1)

    def test_get_image_url_hash(self):
        """It tests that a sha1 hash is generated using image_url attribute."""

        # Testing that dummy image url hash matches.
        self.assertEqual('58dd932ab7127fae6a502a559f6f4fffc9d4a06a',
                         self.dummy_image.image_url_hash)

    def test_image_filename(self):
        """It tests that image_filename property returns an absolute path
        to the location where the downloaded image should be stored.
        """

        # Making sure that generated image filename is correct.
        self.assertEqual(
            os.path.join(settings.IMAGES_ROOT, self.dummy_image.image_filename),
            self.dummy_image.image_filename)

    def test_file_mapper(self):
        """It tests that file_mapper property constructs a dictionary for
        filename creation.
        """

        # Testing that file mapper is generated correctly.
        self.assertEqual({
            'images_root': settings.IMAGES_ROOT,
            'image_hash': '58dd932ab7127fae6a502a559f6f4fffc9d4a06a',
            'file_extension': '.png'}, self.dummy_image.filename_mapper)

    def test_retrieve_image_url(self):
        """It tests that an image file is downloaded from image_url instance
        attribute.
        """

        # Downloading test image from test url.
        self.dummy_image.retrieve_image_url()

        # Testing that image was downloaded to images root.
        self.assertTrue(os.path.exists(self.dummy_image.image_filename))

    def test_thumb_filename(self):
        """It tests that thumbnails file names with the correct suffix."""

        # Testing suffix for thumbnail with aspect ratio.
        self.assertEqual('58dd932ab7127fae6a502a559f6f4fffc9d4a06a.thumb.jpg',
                         self.dummy_image.thumb_filename())

        # Testing suffix for square thumbnail with no aspect ratio.
        self.assertEqual('58dd932ab7127fae6a502a559f6f4fffc9d4a06a.sqthumb.jpg',
                         self.dummy_image.thumb_filename(1))

    def test_generate_image_thumbnails(self):
        """It tests that 2 thumbnails are correctly generated for the downloaded
        image file.
        """

        # Downloading image from url.
        self.dummy_image.retrieve_image_url()

        # Generating thumbnails
        self.dummy_image.generate_image_thumbnails()

        # Testing that thumbnails where generated correctly in the specified
        # location.
        self.assertTrue(os.path.exists(
            settings.THUMBS_ROOT + '/' +
            '58dd932ab7127fae6a502a559f6f4fffc9d4a06a.thumb.jpg'))

        self.assertTrue(os.path.exists(
            settings.THUMBS_ROOT + '/' +
           '58dd932ab7127fae6a502a559f6f4fffc9d4a06a.sqthumb.jpg'))

    def test_get_thumbnails_urls(self):
        """Returns a dict object containing two (key, value) pairs representing
        the ImageUrl instance thumbnails urls."""

        # Expected results
        image_thumbs_urls = {
            'thumb': '/static/img/thumbs/'
                     '58dd932ab7127fae6a502a559f6f4fffc9d4a06a.thumb.jpg',
            'sqthumb': '/static/img/thumbs/'
                       '58dd932ab7127fae6a502a559f6f4fffc9d4a06a.sqthumb.jpg'}

        # Executing test.
        self.assertEqual(image_thumbs_urls, self.dummy_image.thumbnails_urls)

