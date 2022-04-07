#!/bin/bash
#
# This file is copied into the Docker container and is used to both:
# - spin up the email backups job in the background
# - launch the webserver and listen to requests on port 8000
#
# since we're running as a non-root user, we need to run the web server on a non-port (i.e., > 1024).
# we use port forwarding to map port 8000 in the container to port 80 on the host
# - an even better move would be to use port 8000 on the host and use port forwarding on the EC2 firewall
pushd /django_ec2
python email_backups.py &
python manage.py runserver 0.0.0.0:8000
