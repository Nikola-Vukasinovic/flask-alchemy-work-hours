# Flask app for logging & reporting work hours

This is an demo app for logging and reporting work hours inside company. Currently app supports features like user registiration, user managament, work hours entry and review of past work.


### Prerequisites

App has been developed & tested under venv with Python version 3.12. For the full list of needed packages review requirements. 

App uses SQLAlchemy for storage level along with Migration feature.

For app scaling features Flask Blueprinting was employed.


### Requirements

Project includes requirements.txt that can be installed with

```
pip install -r requirements.txt
```


### Environment variables

In order to setup and run following enviroment variables need to be set:

```
ENVIRONMENT=
DEBUG_LEVEL=
ADMIN_NAME=
ADMIN_PASS=
SECRET_KEY=
```
