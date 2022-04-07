FROM python:3.6-alpine
RUN apk add --no-cache \
  bash \
  gcc \
  musl-dev \
  python3-dev

# we run as a non-root user to mitigate the possibility of using a Docker root shell to obtain root on the host
# - note that we also create a user with the same uid (1000) as ec2-user to avoid permissions issues when mounting files
RUN adduser django \
  --disabled-password \
  --shell /bin/bash \
  --uid 1000
USER django
ENV PATH "/home/django/.local/bin:${PATH}"

# install the requirements for the app
WORKDIR /django_ec2
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy the app itself before fixing permissions
COPY . .
USER root
RUN chown -R django:django /django_ec2
USER django

# build the static resources (without this, the production server will fail)
RUN . deploy/env && python manage.py collectstatic

# since we're running as a non-root user, we need to run the web server on a non-port (i.e., > 1024).
# we use port forwarding to map port 8000 in the container to port 80 on the host
# - an even better move would be to use port 8000 on the host and use port forwarding on the EC2 firewall
CMD ["/django_ec2/docker/serve.sh"]
