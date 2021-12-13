# Based on: https://runnable.com/docker/python/dockerize-your-flask-application
FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt

COPY Readme.md requirements.txt /usr/src/app/
COPY tmm/ /usr/src/app/tmm
COPY test/ /usr/src/app/test

WORKDIR /usr/src/app/tmm

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
