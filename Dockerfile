FROM python:3.6-alpine
USER django
RUN apk add --no-cache \
  gcc \
  musl-dev
  python3-dev \

ADD . /django_ec2
WORKDIR /django_ec2

RUN pip install -r requirements.txt

# RUN export $(cat .env) && python manage.py makemigrations
# RUN export $(cat .env) && python manage.py migrate

CMD python manage.py runserver 0.0.0.0:80
