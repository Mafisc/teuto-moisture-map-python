# Based on: https://runnable.com/docker/python/dockerize-your-flask-application
FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt

COPY tmm/app.py /usr/src/app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
