# datapipe

This tool is a django application, i.e. the backend code is written in python. So far, it takes in an email address and class description from the user. It scrapes Google Images for pictures belonging to the class, and stores them in a tar on the cloud. In the future, it should train a generative model using this dataset, and then generate new images, to avoid intellectual property issues. Generative model code is located in [another repository](https://github.com/yousufzu/vae), but would need to be hooked up with this application (and run on a server that has GPUs) in order to work automatically. 

To run: `python3 manage.py runserver`

The various files and what they are for:

## datapipe/templates/datapipe/index.html

This is the HTML for the main page of the tool. Uses bootstrap for the UI, and a vanilla JS XMLHTTPRequest to communicate with the backend.

## datapipe/views.py

The `submit` function here is where the code execution goes after the user clicks submit. It starts the job, and returns an HTTP status 202 to the browser. The user can go do other stuff now.

## datapipe/datapipe.py

Forks off a new process. Calls a function to scrape Google Images and get a list of URLs to pictures of the object. Then it goes through and downloads them and saves them into a tar file, which is uploaded to Google cloud storage. The URL from this upload can be emailed to the user, although this functionality has not been implemented yet.

## datapipe/scraper_google.py

Helper code to find URLs of images from Google Images. Uses Selenium to run a web scraper.

## datapipe/urls.py

This is a django file. It's what hooks up the HTTP request to /submit with the `submit` functions in views.py.

## datapipe/static/datapipe/js/*

Bootstrap UI stuff.
