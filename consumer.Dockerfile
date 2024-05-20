FROM ubuntu:latest

WORKDIR /api

COPY ./api/modeling/saved-models /api/saved-models
COPY ./api/requirements.txt /api/requirements.txt
COPY ./api/consumer.py /api/consumer.py

RUN apt update
RUN apt install -y wget curl
RUN wget https://download.oracle.com/java/17/latest/jdk-17_linux-x64_bin.deb
RUN apt install ./jdk-17_linux-x64_bin.deb
RUN rm jdk-17_linux-x64_bin.deb
ENV JAVA_HOME=/usr/lib/jvm/jdk-17-oracle-x64

RUN apt install -y software-properties-common build-essential nano
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update
RUN apt install -y python3.10 python3.10-distutils python3-pip
RUN pip install --no-cache-dir -r requirements.txt --ignore-installed --break-system-packages
RUN python3 -m nltk.downloader stopwords

CMD python3 consumer.py