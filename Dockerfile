FROM python3.9

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
CMD flask run --host 0.0.0.0
