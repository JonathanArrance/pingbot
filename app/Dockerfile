FROM python:3.8.2-slim-buster
MAINTAINER Jonathan Arrance <jonathan@thesingleboard.io>

ENV INSTALL_PATH /opt/pingbot

RUN apt-get update -y;apt-get install -y curl;apt-get install -y python3-pip;apt install -y python3-dev;apt install -y git;apt install -y iputils-ping;apt install -y dnsutils

WORKDIR $INSTALL_PATH

RUN pip3 install --upgrade pip
ADD requirements.txt /
RUN pip3 install -r /requirements.txt

ADD pingbot.py $INSTALL_PATH
ADD pingbot_lib.py $INSTALL_PATH
ADD run_app.py $INSTALL_PATH
ADD entrypoint.sh $INSTALL_PATH
ADD settings.py $INSTALL_PATH

#PROM port
EXPOSE 9002

ENTRYPOINT ["python3","run_app.py"]
