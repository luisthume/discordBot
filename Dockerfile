# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.7

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

RUN apt update && apt install -y vim gcc pkg-config openssl libcurl4-openssl-dev libssl-dev apache2 apache2-dev libapache2-mod-wsgi-py3
RUN apt update && apt install -y build-essential libssl-dev libffi-dev python3-dev
RUN apt update && apt install -y unixodbc-dev

# create root directory for our project in the container
RUN mkdir /app

# Set the working directory to /music_service
WORKDIR /app

# Copy the current directory contents into the container at /music_service
ADD . /app/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt