# WillBuyer [![Build Status](https://travis-ci.com/willrp/willbuyer.svg?branch=master)](https://travis-ci.com/willrp/willbuyer) [![Coverage Status](https://coveralls.io/repos/github/willrp/willbuyer/badge.svg?branch=master)](https://coveralls.io/github/willrp/willbuyer?branch=master)

WillBuyer is a demonstration project to show and sell other e-commerce platforms' goods. It is a Service Oriented Architecture and Rich Internet application, build using the MVCS architectural pattern (Model View Controller Service). The merchandise data WS comes from [ASOS Online Shopping](https://www.asos.com), outlet sections.

This project uses DevOps practices, it's tested on TravisCI, coverage checked by Coveralls and automatically deployed on Heroku. In this application, the following tests are made:

* Unit tests;
* Integration tests;
* Functional tests.

You can access the API documentation [here](http://willbuyer.herokuapp.com/api). The application Frontend will be built soon.
Since it uses free dynos, it might take some seconds for the first access. Thank you for understanding.

## Own Dependent Web services

* [WillOrders](https://github.com/willrp/willorders-ws): Manages the orders made by the customers;
* [WillStores](https://github.com/willrp/willstores-ws): Provides information about the products available in the store.

## Back end built with

* [Blinker](https://github.com/jek/blinker): A fast Python in-process signal/event dispatching system;
* [Flask](http://flask.pocoo.org): Web applications framework for Python. For managing the routes and web services. For project backend control and model layers;
* [Flask-Dance](https://github.com/singingwolfboy/flask-dance): Authentication with Oauth2;
* [Flask-Login](https://github.com/maxcountryman/flask-login): Flask user session management;
* [Flask-Restplus](https://github.com/noirbizarre/flask-restplus): An extension for Flask that adds support for quickly building REST APIs expose its documentation properly;
* [Flask-Talisman](https://github.com/GoogleCloudPlatform/flask-talisman): HTTP security headers for Flask;
* [Marshmallow](https://github.com/marshmallow-code/marshmallow): A lightweight library for converting complex objects to and from simple Python datatypes. For input JSON payload validation;
* [Python](https://www.python.org): Main backend programming language. For Web services control, service and model layers;
* [Python-dotenv](https://github.com/theskumar/python-dotenv): Get and set values in your .env file in local and production servers;
* [Pipenv](https://github.com/pypa/pipenv): Package manager for Python programming language;
* [PostgreSQL](https://www.postgresql.org/): A powerful, open source object-relational database system;
* [Psycopg2](https://github.com/psycopg/psycopg2): PostgreSQL database adapter for the Python programming language;
* [Requests](https://github.com/requests/requests): For making server HTTP requests;
* [SQLAlchemy](https://www.sqlalchemy.org/): Python SQL toolkit and Object Relational Mapper.

## Front end built with

COMING SOON

## Development tools

* [Click](https://github.com/pallets/click): Python composable command line interface toolkit;
* [Docker](https://www.docker.com/): Performs web services containerization, helping on application development, integration tests and production. Boosts production by getting everything started easily and isolated, and reloading the application on code change;
* [PyOpenSSL](https://github.com/pyca/pyopenssl): A Python wrapper around the OpenSSL library.

## Testing tools

* [Coveralls](https://coveralls.io): A hosted analysis tool, providing statistics about your code coverage;
* [Coveralls-python](https://pypi.org/project/coveralls/): Integration between Python and coveralls;
* [Elasticsearch](https://www.elastic.co): A distributed, RESTful search and analytics engine. To store and search data;
* [Elasticsearch DSL](https://github.com/elastic/elasticsearch-dsl-py): A high-level library to write and run queries against Elasticsearch for Python;
* [Factory Boy](https://github.com/FactoryBoy/factory_boy): A fixtures replacement tool, aiming to replace static, hard to maintain fixtures with easy-to-use factories for complex objects;
* [Pytest](https://github.com/pytest-dev/pytest): A mature full-featured Python testing tool that helps you write better programs;
* [Pytest-cov](https://github.com/pytest-dev/pytest-cov): A plugin to produce coverage reports for Pytest;
* [Pytest-mock](https://github.com/pytest-dev/pytest-mock): Thin-wrapper around the mock package for easier use with Pytest;
* [Responses](https://github.com/getsentry/responses): A utility for mocking out the Python Requests library;
* [TravisCI](https://travis-ci.com): A hosted continuous integration service used to build and test software projects;
* [VCRpy](https://github.com/kevin1024/vcrpy): Automatically mock HTTP interactions to simplify and speed up testing.

## Production tools

* [Gunicorn](https://gunicorn.org/): A Python WSGI HTTP Server for UNIX;
* [Heroku](https://www.heroku.com/): A platform as a service (PaaS) that enables developers to build, run, and operate applications entirely in the cloud.

## Author

Engineered and coded by:
* **Will Roger Pereira** - https://github.com/willrp

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.