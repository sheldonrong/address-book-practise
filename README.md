# Address Book Manager - Back end

[For details about how front end is built, please check the [\[Front End Readme\]](./frontend/)]

Flask application with Open API (Swagger) standard compatible RESTful API.

### Demo

This application has been deployed to Google App Engine at:
`https://address-book-196923.appspot.com/`

### Installing

Create a new Python 3.5 virtualenv, and activate the env and run `pip install -r requirements.txt`.

For Google App Engine deployment, see the `app.yaml` file.

### Deployment

Set the Flask application global variable `FLASK_APP` to `app.py` and then simply execute `flask run` in the command line.

### Built With

* `Python 3`
* `Flask`
* `SQLAlchemy`
* `Alembic` for database migration
* `Flask-RESTPLUS` for Swagger compatible RESTful API
* `PostgreSQL` for database
* `nosetests` for unit tests (86% coverage)

### Endpoints
* `/ ` root for the main application
* `/api` RESTful API endpoint
* `/api_doc` Swagger RESTful API documentation

### Authors
Sheldon Rong

### A bit about Google App Engine

First of all, I have to say `gcloud app deploy` really takes a lot of time. (and it seems a lot of people are not happy :) )

Then there is a second issue I managed to solve, and it was caused by non-other than autoscaling.

Sometimes you love autoscaling, sometimes you don't :)

So the issue is: when the app is running in GAE, and when user upload the CSV file, there is about half chance you
get an error immediately after the file finished uploading, saying could not locate the file.

Initially I thought this is related to files sitting in /tmp or /var/tmp being aggressively deleted by the OS.
So had a bit tweeting of both code and the linux settings. Ha, I was so wrong.
It turns out Google auto scaled my instance, and when the file is uploaded, it is saved as a copy in one
of the instance container, not both. So that sort of explained why it is an intermittent issue.

Now obviously, this means there is a design flaw here, and to solve this, files has to be uploaded to a central
server, and in Google's case, the Google Cloud Storage, which would then need to use the SDK to connect.
However, due to limited time, I decided to go the other approach: remove one of the instance.

With this in mind, here are the details.

### License
This project is licensed under the MIT License
