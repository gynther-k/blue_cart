FROM ubuntu:bionic

WORKDIR /usr/src/app

RUN apt-get update -y

RUN apt-get install -y python3-pip gzip

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY ./src .

EXPOSE 3000

ENV PYTHONUNBUFFERED=0

CMD [ "python3","-u","server.py" ]

