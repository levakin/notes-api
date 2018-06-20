
# RESTful Notes API

Simple RESTful service to post notes.

Interact with the app using HTTP methods:
* GET - to get all the notes
* POST - to post a note
* PUT - to update note
* DELETE - to delete note

SwaggerUI will provide more information if you run the app. See doc on [URL localhost:8080/doc](localhost:8080/doc) 
while running the app.
![SwaggerUI](https://raw.githubusercontent.com/Levakin/notes-api/master/imgs/doc.png)
## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development
 and testing purposes. See deployment for notes on how to deploy the project using Docker.

### Prerequisites

Python3 should be installed. Before you go any further, make sure you have Python and that it’s available 
from your command line. You can check this by simply running:
```
$ python --version
```
Additionally, you’ll need to make sure you have pip available. You can check this by running:
```
$ pip --version
```

[Pipenv](https://docs.pipenv.org/) is needed to make virtual environment and install dependencies. 

```
$ pip install --user pipenv
```

Note:

This does a user installation to prevent breaking any system-wide packages. If pipenv isn’t available in your shell 
after installation, you’ll need to add the user base’s binary directory to your PATH. 
[more info](https://docs.pipenv.org/install/#installing-pipenv)
### Installing

Cd in the directory.

```
$ cd notes-api
```

Make virtual environment and install requirements with pipenv:

```
$ pipenv install
```

To activate virtual environment use the following command:

```
$ pipenv shell
```

To exit the env:

```
$ exit
```

## Running the application
Use these commands while in the virtual environment:
```
$ pipenv shell
```
* To start the application:
```
$ flask run
```
* To add examples into database use the following:
```
$ flask add_examples
```
The server will be available on the [localhost](localhost:8080) 8080 port. 

RESTPlus adds the SwaggerUI documentation that is available using the URL [localhost:8080/doc](localhost:8080) 

* To empty database:
```
$ flask empty
```
* To empty database and add examples:
```
$ flask reset
```


## Docker

You can download docker image from the docker registry using the following command
```
$ docker pull levakin/notes-api
```
or you can build image yourself
```
$ docker build -t notes-api .
```
To run container named notes-container from image use the following command:
 ```
$ docker run -d --name notes-container -p 8080:8080 levakin/notes-api flask run
```
Server will be running on the [localhost:8080](localhost:8080)
To execute commands in container:
 ```
$ docker exec notes-container COMMAND
```
Example:
 ```
$ docker exec notes-container flask reset
```
To stop container:
 ```
$ docker stop notes-container
```
To start container and server again:
 ```
$ docker start notes-container && docker exec notes-container flask run
```
## Built With

* [Flask](http://flask.pocoo.org/docs/1.0/) - Flask is a microframework for Python based on Werkzeug,
 Jinja 2 and good intentions.
* [Flask-RESTPlus](https://flask-restplus.readthedocs.io/en/stable/) - Flask-RESTPlus is an extension for Flask
 that adds support for quickly building REST APIs. 
* [Marshmallow](https://marshmallow.readthedocs.io/en/stable/) - marshmallow is an ORM/ODM/framework-agnostic 
library for converting complex datatypes, such as objects, to and from native Python datatypes.
* [SQLAlchemy](http://docs.sqlalchemy.org/en/latest/) - The SQLAlchemy SQL Toolkit and Object Relational
 Mapper is a comprehensive set of tools for working with databases and Python.


## Authors

* **Anton Levakin** - *Initial work* - [Levakin](https://github.com/Levakin)

## License

This project is licensed under the Apachem 2.0 License - see the [LICENSE.md](LICENSE.md) file for details



