# datapipe

This tool is a django application, i.e. the backend code is written in python.

To run: `python manage.py runserver`

The various files and what they are for:

##datapipe/templates/datapipe/index.html

This is the HTML for the main page of the tool. Uses bootstrap for the UI, and a vanilla JS XMLHTTPRequest to communicate with the backend.

##datapipe/views.py

The `submit` function here is where the code execution goes after the user clicks submit.
