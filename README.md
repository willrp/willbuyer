# WillBuyer [![Build Status](https://travis-ci.com/willrp/willbuyer.svg?branch=master)](https://travis-ci.com/willrp/willbuyer) [![Coverage Status](https://coveralls.io/repos/github/willrp/willbuyer/badge.svg?branch=master)](https://coveralls.io/github/willrp/willbuyer?branch=master)

WillBuyer is a demonstration project to show and sell other e-commerce platforms' goods. It is a Service Oriented Architecture and Rich Internet application, build using the MVCS architectural pattern (Model View Controller Service),and a responsive design, for any device. The merchandise data comes from [ASOS Online Shopping](https://www.asos.com), outlet sections.

[Click here to access the application.](http://willbuyer.herokuapp.com)

This project uses DevOps practices, it's tested on TravisCI, coverage checked by Coveralls and automatically deployed on Heroku. In this application, the following tests are made:

* Unit tests;
* Integration tests;
* Functional tests.

The application is available [in this link](http://willbuyer.herokuapp.com). You can also access the API documentation [here](http://willbuyer.herokuapp.com/api).
Since it uses free dynos, it might take some seconds for the first access. Thank you for understanding.

## Own Dependent Web services

* [WillOrders](https://github.com/willrp/willorders-ws): Manages the orders made by the customers;
* [WillStores](https://github.com/willrp/willstores-ws): Provides information about the products available in the store.

## Back end built with

* [Asyncio](https://docs.python.org/3/library/asyncio.html): A Python library to write concurrent code using the async/await syntax;
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

* [Axios](https://github.com/mzabriskie/axios): For making frontend HTTP requests with AJAX;
* [Babili Minify Webpack Plugin](https://github.com/webpack-contrib/babili-webpack-plugin): For JS and ES6 code minification;
* [Clean for Webpack](https://github.com/johnagan/clean-webpack-plugin): A webpack plugin to remove/clean your build folder(s) before building;
* [CSS](https://www.w3schools.com/css): An HTML styler. To style data shown to the user. For project frontend view layer;
* [ECMAScript](https://tc39.github.io/ecma262/): A script-language, for frontend programming, with new syntax for writing complex applications. Works very well with ReactJS;
* [Emotion](https://github.com/emotion-js/emotion): A performant and flexible CSS-in-JS library;
* [Flow](https://flow.org): Static type checker for Javascript;
* [HTML](https://www.w3schools.com/html): A markup language to build webpages. To show data to the user. For project frontend view layer;
* [HTML Webpack Plugin](https://github.com/jantimon/html-webpack-plugin): Plugin that simplifies creation of HTML files to serve your bundles;
* [Javascript](https://www.javascript.com): A web browser client-side programming language. To process data at client side, control user events and struture the view. For project frontend control layer;
* [Lodash](https://github.com/lodash/lodash): A modern JavaScript utility library delivering modularity, performance, & extras;
* [MiniCSS Extract Plugin](https://github.com/webpack-contrib/mini-css-extract-plugin): Extracts CSS into separate files. It creates a CSS file per JS file which contains CSS. It supports On-Demand-Loading of CSS and SourceMaps;
* [Moment](https://github.com/moment/moment/): Parse, validate, manipulate, and display dates and times in JavaScript;
* [Npm](https://www.npmjs.com): A package manager for the JavaScript programming language and related. Bundled with NodeJS;
* [Optimize CSS Assets Webpack Plugin](https://github.com/NMFR/optimize-css-assets-webpack-plugin): A Webpack plugin to optimize and minimize CSS assets;
* [Query-String](https://github.com/sindresorhus/query-string): Parse and stringify URL query strings;
* [RC Slider](https://github.com/schrodinger/rc-slider): React slider;
* [ReactJS](https://facebook.github.io/react): A Javascript library for building user interfaces. To struture the view on components. For project frontend control and layer;
* [React-Dates](https://npmjs.org/package/react-dates): An easily internationalizable, mobile-friendly datepicker library for the Web;
* [React Image Gallery](https://github.com/xiaolin/react-image-gallery): React image gallery component with thumbnail support; 
* [React-NProgress](https://www.npmjs.com/package/react-nprogress): Slim progress bars for Rich Internet Applications;
* [React-Router](https://github.com/ReactTraining/react-router): Declarative routing for ReactJS. For state URL management;
* [React Slick](https://github.com/akiran/react-slick): React carousel component;
* [React-Toastify](https://github.com/fkhadra/react-toastify): Notifications for ReactJS;
* [Semantic-UI-React](https://github.com/Semantic-Org/Semantic-UI-React): A framework that helps create beautiful, responsive layouts using human-friendly HTML, integrated with ReactJS;
* [Webpack](https://webpack.js.org/): A JavaScript module bundler. Bundles JS, CSS and images, as well as gives support for other plugins.

## Development tools

* [Click](https://github.com/pallets/click): Python composable command line interface toolkit;
* [Docker](https://www.docker.com/): Performs web services containerization, helping on application development, integration tests and production. Boosts production by getting everything started easily and isolated, and reloading the application on code change;
* [PyOpenSSL](https://github.com/pyca/pyopenssl): A Python wrapper around the OpenSSL library;
* [React Developer Tools](https://github.com/facebook/react-devtools): To inspect the React component hierarchy including props and state. Also helps inpecting if the build is production ready. Browser extension needs to be installed;
* [React Hot Loader](https://github.com/gaearon/react-hot-loader): A tool to update your application while developing, automatically, without losing state. Boosts production and allow to tweak React components in real time;
* [Webpack Bundle Analyzer](https://github.com/webpack-contrib/webpack-bundle-analyzer): Visualize size of webpack output files with an interactive zoomable treemap;
* [Webpack Dev Server](https://github.com/webpack/webpack-dev-server): Use Webpack with a development server;
* [Write File Webpack Plugin](https://github.com/gajus/write-file-webpack-plugin): Forces webpack-dev-server to write bundle files to the file system.

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