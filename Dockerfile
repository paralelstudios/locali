FROM tiangolo/uwsgi-nginx-flask:flask-python3.5

MAINTAINER Michael Perez "mpuhrez@paralelstudios.com"

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN pip install -e .
