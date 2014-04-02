from django.shortcuts import render
from core.forms import JsonForm
from core import tasks


def create_images(request):
    """This api call triggers a task to process new JSON input."""

    # Saving session cookie.
    request.session.save()

    # Triggers a task that will create image items in the server from correctly
    # formed JSON.
    if request.method == 'POST':
        # Verifying the posted JSON it's correctly formed.
        form = JsonForm(request.POST)
        if form.is_valid():
            parsed_json = form.cleaned_data['images_json']
            # Triggering an asynchronous task.
            for id, image_data in parsed_json.items():
                tasks.create_image.apply_async(
                    args=[request.session.session_key],
                    kwargs=image_data)

    # Initialize an empty JSON form.
    elif request.method == 'GET':
        form = JsonForm(initial={'images_json': JsonForm.initial_json()})

    return render(request, 'index.html', {'form': form})
