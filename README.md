# <a href="https://www.fosterloveproject.org/" target="_blank">FLP Inventory Platform</a>

* Organization: Foster Love Project
* Client Contacts: <a href="mailto:khughes@fosterloveproject.org">`Kelly Hughes`</a>, <a href="mailto:ebaldoni@fosterloveproject.org">`Elizabeth Baldoni`</a>, <a href="mailto:center@fosterloveproject.org">`Krissy Evans`</a>
* Student Consultants: <a href="https://github.com/alex-bellomo">`Alex Bellomo`</a>, <a href="https://github.com/mkornyev">`Max Kornyev`</a>, <a href="https://github.com/austin-leung">`Austin Leung`</a>, <a href="https://github.com/lydiaxing">`Lydia Xing`</a>, and <a href="https://github.com/SeanEZhou">`Sean Zhou`</a>

### Application Versions

* `Python 3.6.6`
* `Django 3.1.7`
* See `requirements.txt` for a complete enumaration of package dependencies

***

### Dependency Setup (DEVELOPMENT)

The following will set up a python environment for this project using `virtualenv` . This allows us to keep all your project dependencies (or `pip modules`) in isolation, and running their correct versions. 

* If you dont have `virtualenv` install: `pip install virtualenv`
* In the project directory, create the env: `virtualenv djangoEnv` (set djangoEnv to your preferred env name)
  * it is already added in the gitignore
* Start the env: `source djangoEnv/bin/activate`
* Install all dependencies: `pip install -r requirements.txt`
* Exit the env: `deactivate` or `exit` terminal 
* **FOR DEVELOPMENT: After installing new python libraries to your pipenv, you must update the `requirements.txt` file**
	* Do this by running `pip freeze > requirements.txt` AFTER you have started the environment

<hr></hr>

## THE FOLLOWING HAVE NOT YET BEEN WRITTEN

### Test Suite 

* Run the suite with `./manage.py test`

### Included Scripts 

###### Populate

* `python manage.py populate`

###### Drop

* `python manage.py drop`
	* Destroys all objects 
