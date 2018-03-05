# Address Book Manager - Back end

For setting up front end of this demo, please check the [\[Front End Readme\]](./frontend/)

Flask application with Open API (Swagger) standard compatible RESTful API.

### Demo

This application has been deployed to Google App Engine at:
`https://address-book-196923.appspot.com/`

I have to say `gcloud app deploy` takes quite a lot of time to finish each time.

### Installing

It's Python, no need for installation!

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

### License
This project is licensed under the MIT License
