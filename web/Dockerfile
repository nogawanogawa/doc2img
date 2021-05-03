FROM python:3.7

WORKDIR /app/src

RUN apt update
RUN apt install -y curl 
RUN apt install -y poppler-utils
RUN apt install -y unoconv imagemagick
RUN apt install -y fonts-ipafont fonts-ipaexfont

COPY requirements.txt /app/src
RUN pip3 install -r requirements.txt


