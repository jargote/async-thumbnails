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
        data = self.data['images_json']
        try:
            parsed_json = json.loads(data)
        except json.JSONDecodeError as e:
            raise forms.ValidationError(e.message)
        else:
            return parsed_json

    @classmethod
    def inital_json(cls):
        return json.dumps(cls.INITIAL)