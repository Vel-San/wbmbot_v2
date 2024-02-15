# Use a minimal Ubuntu base image
FROM ubuntu:latest

LABEL VERSION="1.0.1"
LABEL MAINTAINER="Vel-San | vel-san@protonmail.com"
LABEL DESCRIPTION="A docker image that has all required dependenices for the bot to run"

# ARGS
ARG DEBIAN_FRONTEND=noninteractive

# Update package lists and install necessary packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    nano \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /home

# Copy the Python project files into the container
COPY configs/ /home/configs
COPY logging/ /home/logging
COPY offline_viewings/ /home/offline_viewings
COPY wbmbot_v2/ /home/wbmbot_v2

# Install project dependencies
RUN pip3 install --no-cache-dir -r /home/wbmbot_v2/requirements.txt

# Command to run the bot
CMD ["python3", "/home/wbmbot_v2/main.py", "-H"]
