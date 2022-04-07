# <a href="https://www.fosterloveproject.org/" target="_blank">FLP Inventory Platform</a>

* Organization: Foster Love Project
* Client Contacts: <a href="mailto:khughes@fosterloveproject.org">`Kelly Hughes`</a>, <a href="mailto:ebaldoni@fosterloveproject.org">`Elizabeth Baldoni`</a>, <a href="mailto:center@fosterloveproject.org">`Krissy Evans`</a>
* Student Consultants: <a href="https://github.com/alex-bellomo">`Alex Bellomo`</a>, <a href="https://github.com/mkornyev">`Max Kornyev`</a>, <a href="https://github.com/austin-leung">`Austin Leung`</a>, <a href="https://github.com/lydiaxing">`Lydia Xing`</a>, and <a href="https://github.com/SeanEZhou">`Sean Zhou`</a>
* The beta deployment is at <a href="https://flp-app.herokuapp.com/">flp-app.herokuapp.com</a>

### Application Versions

* `Python 3.6.6`
* `Django 3.1.7`
* See `requirements.txt` for a complete enumaration of package dependencies

***

### Dependency Setup (DEVELOPMENT)

The following will set up a python environment for this project using `virtualenv`.
This allows us to keep all your project dependencies (or `pip modules`) in isolation, and running their correct versions.

* If you dont have `virtualenv` install: `pip install virtualenv`
* In the project directory, create the env: `virtualenv djangoEnv` (set djangoEnv to your preferred env name)
  * it is already added in the gitignore
* Start the env: `source djangoEnv/bin/activate`
* Install all [new] dependencies: `pip install -r requirements.txt`
* Exit the env: `deactivate` or `exit` terminal 
* **FOR DEVELOPMENT: After installing new python libraries to your pipenv, you must update the `requirements.txt` file**
	* Do this by running `pip freeze > requirements.txt` AFTER you have started the environment

### Running The App 

* If you created some new models:
  * `python manage.py makemigrations inventory` && `python manage.py migrate`
* Run the app: `python manage.py runserver` ~> <a href="http://localhost:8000/">localhost:8000</a>

<hr></hr>

### Included Scripts 

##### Admin

* `python manage.py createsuperuser`
	* Create an admin username and password
* Log into admin view at <a href="http://localhost:8000/admin/">localhost:8000/admin/</a>

###### Populate

* `python manage.py populate`
	* Creates sample model data for testing 
	* Creates a superuser login: `<username>:<pass>` | `admin:admin`
	* Creates a staff login: `<username>:<pass>` | `staff:staff`

###### Drop

* `python manage.py drop`
	* Destroys all objects 

### Test Suite 

* Run the suite with `./manage.py test`

### Deployment (First-Time)

* To SSH into AWS, you can find our private key file in Google Drive and use the AWS login credentials in the handoff doc to get the public DNS

* Deployment tutorial: https://stackabuse.com/deploying-django-applications-to-aws-ec2-with-docker - also please make sure you turn off debug mode in settings.py, check out our deployment PR to see what changes you gotta make and save the .sqlite3 db file before you run `docker pull` so you don't overwrite FLP's data

* Use `docker exec` to run `source .env` (.env file in the google drive) and all of the following commands

* Next, run `python manage.py drop` then `python manage.py import MANAGE_INVENTORY_FILE MANAGE_ITEMS_FILE` (these are also in the google drive)

* Run `email_backups.py &` to send db backup emails weekly

* Make starter staff superuser and volunteer account

* Finally run the server on port 80 (still using docker exec, `python manage.py runserver 80`. For exact commands you can scroll the bash history)


### Deployment (Ongoing)

The AWS/EC2 deployment of the FLP Inventory app is managed using Docker Compose.
You will need to ensure that the SQLite database file, `db.sqlite3`, is moved into the `deploy` directory.
Additionally, you will need to copy the `env` file from Google Drive (containing deployment secrets) to the `deploy` directory (i.e., `deploy/env`).
To launch the server, you should run:

	$ docker-compose up -d

To check on the state of the server via its logs, you can run:

	$ docker-compose logs

To shutdown the server, you should run:

	$ docker-compose down

To restart an already-running server, you should run:

	$ docker-compose restart

Note that all of the above commands should be run from the root of this directory.
