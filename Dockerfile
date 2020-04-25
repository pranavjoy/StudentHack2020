FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

RUN python3 --version

RUN pip3 install --upgrade pip

RUN pip3 install flask_pymongo && \
    pip3 install flask && pip3 install numpy && \
    pip3 install pandas && pip3 install nltk && pip3 install scipy

RUN apt-get install -y locales locales-all

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

RUN apt-get install -y python-scipy

ENV LANG C.UTF-8

ENV LC_ALL C.UTF-8

ENV FLASK_APP hardboiled

COPY . /app

CMD flask run --host='0.0.0.0' -p 80
