FROM python:3.8.5-slim-buster

WORKDIR /usr/src/app

RUN apt-get update -y

RUN apt-get install -y gzip

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./src .

EXPOSE 3000
EXPOSE 5672

CMD [ "python","-u","server.py" ]

