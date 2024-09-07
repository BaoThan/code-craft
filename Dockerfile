# Download base image Ubuntu
FROM ubuntu:latest

# Disable Prompt During Packages Installation
ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /app

COPY requirements.txt .

# Update Ubuntu software repository
RUN apt-get update
RUN apt update

#==============================================================================
# Install programming languages compilers/interpreters needed
#==============================================================================
# C
RUN apt-get install -y gcc
# C++
RUN apt-get install -y g++
# C#
RUN apt install -y mono-complete
# Java
RUN apt install -y default-jdk
# Javascript
RUN apt-get install -y nodejs
# Python3
RUN apt-get install -y python3.10 python3-venv
# Ruby
RUN apt-get install -y ruby-full
# PHP
RUN apt-get install -y php
# Go
RUN apt-get install -y golang-go
# Rust
RUN apt-get install -y rustc

# Install pip package manager for python
RUN apt-get install -y python3-pip

# Create and activate a virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install required python libraries
RUN python3 -m pip install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5000"]
