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

You will follow these directions if there is no EC2 instance created with a docker image running:

* To SSH into AWS, you can find our private key file in Google Drive and use the AWS login credentials in the handoff doc to get the public DNS

* Deployment tutorial: https://stackabuse.com/deploying-django-applications-to-aws-ec2-with-docker - also please make sure you turn off debug mode in settings.py, check out our deployment PR to see what changes you gotta make and save the .sqlite3 db file before you run `docker pull` so you don't overwrite FLP's data (Note: Do not follow the `docker run` commands, use 'docker-compose build` to build as this application now runs using a docker-compose file. 

* Make sure in `deploy`, you have the `db.sqlite3`, `env` files from the Google Drive. Furthermore, add the `settings.yaml` file for Exporting to Google Drive functionality in the root directory (`/home/ec2-user/github`) of where the repository is stored.

* Next, run `python manage.py drop` then `python manage.py import MANAGE_INVENTORY_FILE MANAGE_ITEMS_FILE` (these are also in the google drive)

* Run `email_backups.py &` to send db backup emails weekly

* Make starter staff superuser and volunteer account

* Finally run the server after running 'docker-compose build' by running 'docker-compose up -d'

### Deployment (Ongoing)

You will follow these directions if there is an EC2 instance created with a docker image running:

The AWS/EC2 deployment of the FLP Inventory app is managed using Docker Compose.
	
To update the code/website: You will checkout a new branch or pull the new code that you wish to update the EC2 instance/website with. Then, you will need to build the image and volume mounts with the specified command(s) below. Afterwards, you can start the docker with the up command below. A good resource to see past history of commands to verify your process is `cat ~/.bash_history`. This will give you a good sense of how past updates have occurred. 
	
Firstly, you will need to ensure that the SQLite database file, `db.sqlite3`, is moved into the `deploy` directory (i.e. `deploy/env`).
Secondly, you will need to copy the `env` file from Google Drive (containing deployment secrets) to the `deploy` directory (i.e. `deploy/env`).
Finally, you will need to copy the `settings.yaml` file from the Google Drive (containing Google API client ID and secrets) to the root directory (`/home/ec2-user/github`) of the repository (`cd ..` if within the `deploy` directory).

To build the docker image, you should run:

	$ docker-compose build
	
To launch the server, you should run:

	$ docker-compose up -d

To check on the state of the server via its logs, you can run:

	$ docker-compose logs

To shutdown the server, you should run:

	$ docker-compose down

To restart an already-running server, you should run:

	$ docker-compose restart

Note that all of the above commands should be run from the root of this directory (`/home/ec2-user/github`).
