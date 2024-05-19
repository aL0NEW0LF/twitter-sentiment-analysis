FROM ubuntu:latest

WORKDIR /api

COPY ./api/requirements-server.txt /api/requirements.txt
COPY ./api/server.py /api/server.py

RUN apt update
RUN apt install -y wget curl

RUN apt install -y software-properties-common build-essential nano
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update
RUN apt install -y python3.10 python3.10-distutils python3-pip
RUN pip install --no-cache-dir -r requirements.txt --ignore-installed --break-system-packages

EXPOSE 5000

CMD python3 server.py