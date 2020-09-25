FROM python:3.8.5-slim-buster

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

COPY ./src .

RUN apt-get update -y

RUN apt-get install -y gzip

RUN pip install -r requirements.txt

EXPOSE 50051

CMD [ "python", "server.py" ]

