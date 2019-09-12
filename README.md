# AttendanceClock

| Project Name | Codebase | Current Release | Build Status |
| :---: | :---: | :---: | :---: |
| AttendanceClock | https://github.com/omprakash1989/AttendanceClock | - | - |


###### Attendance Clock is a small, dummy application for clock-in and clock-out feature for teachers.


### Technology Stacks

- [Python3.6](https://docs.python.org/)
- [Flask](http://flask.pocoo.org/docs/)
- [Postgresql](https://www.postgresql.org/docs/)


### No Choice on

- [Coding Standard](https://www.python.org/dev/peps/pep-0008/)

- Test Cases (Failure & Success)

- Code Quality


***

# Setup Process

#### Python Library Requirements
All the python library requirements are specified in requirements.txt file.

#### To install the required libraries:

Create Virtual Environment(Optional but suggested):

- virtualenv clockin_env


Work on virtualenv

- source /path-to-clockin_env/bin/activate


Install Dependencies

- `pip install -r requirements.txt`


Setup Flask Environment

- Move to `app` folder inside the project folder.

- Run command on terminal `export $FLASK_APP=wsgi.py`


Handling Configuration

- Create a new file `settings/settings_local.py` if does not exist else update the existing one with details.

- In case there is not local settings file, Copy the all the config vars from `settings/settings_local.py.sample` file. Change the configurations according to requirement.

- *Note*: Any changes in configurations should be added to all environment settings along with the sample settings file.



Database migrations:

- Run command: `flask db upgrade`


Running tests:

- Run command: `py.test`


Running Application

There are couple of way of running the application.


- Run Command: `uwsgi uwsgi.ini` (Suggested)

- Or run command: `flask run` or `python wsgi.py`

***
# Others


### WIP

-


### Frontend
-
