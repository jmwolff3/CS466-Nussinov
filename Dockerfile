FROM python:3.8-slim-buster

LABEL Author="John M. Wolff"
LABEL version="0.0.1"

ENV PYTHONDNTWRITEBYTECODE 1

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

ADD . /app

EXPOSE 5000
CMD python flask_app.py --host=0.0.0.0
