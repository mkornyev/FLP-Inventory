FROM python:3.6-alpine

EXPOSE 80

RUN apk add --no-cache gcc python3-dev musl-dev

ADD . /django_ec2

WORKDIR /django_ec2

RUN pip install -r requirements.txt

RUN export $(cat .env) && python manage.py makemigrations

RUN export $(cat .env) && python manage.py migrate

CMD export $(cat .env) && python manage.py runserver 0.0.0.0:80
