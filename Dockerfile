FROM python:3.6-alpine

EXPOSE 8000

RUN apk add --no-cache gcc python3-dev musl-dev

ADD . /django_ec2

WORKDIR /django_ec2

RUN source .env

ENV EMAIL_APP_PASS=${EMAIL_APP_PASS}

ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}

ENV ADMIN_USER_PASS=${ADMIN_USER_PASS}

ENV STAFF_USER_PASS=${STAFF_USER_PASS}

RUN pip install -r requirements.txt

RUN python manage.py makemigrations

RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
