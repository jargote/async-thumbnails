import simplejson as json

from django import forms


class JsonForm(forms.Form):
    INITIAL = {
        "item1": {
            "title": "Image title",
            "description": "some description",
            "image_url": "/some/url/to/image"
       },
        "item2": {
            "title": "Image title2",
            "description": "some description2",
            "image_url": "/some/url/to/image2"
       }
    }

    images_json = forms.CharField(label='Download Images from JSON',
                                  widget=forms.Textarea)

    def clean_images_json(self):
        """Verifies that given json is correctly formatted."""

        data = self.data['images_json']
        try:
            # Parsing JSON.
            parsed_json = json.loads(data)
        except json.JSONDecodeError as e:
            # Raising validation form error if JSON cannot be decoded.
            raise forms.ValidationError(e.message)
        else:
            return parsed_json

    @classmethod
    def initial_json(cls):
        """Some initial JSON.
        This is intended to be used as reference to a correctly input JSON.
        """

        return json.dumps(cls.INITIAL)