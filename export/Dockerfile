# Based on: https://runnable.com/docker/python/dockerize-your-flask-application
FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app
COPY config.ini /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY export_influx.py /usr/src/app/

WORKDIR /usr/src/app

CMD [ "python3", "export_influx.py" , "config.ini"]