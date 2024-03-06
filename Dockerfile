# Base image - for python environments mostly Python
FROM python:3.11-slim

# set the working directory
WORKDIR /app

# install system dependencies
RUN apt-get update && apt-get install -y \
    libnuma-dev \
    && rm -rf /var/lib/apt/lists/*

# install dependencies
COPY ./requirements.txt ./
COPY ./setup.py ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy the src to the folder
COPY ./src ./src

# Install the package from the local src directory

# RUN pip install -e .

# Common pitfalls:
# 1) Filename has to be Dockerfile exactly. Otherwise it won't work.
# https://python.plainenglish.io/3-simple-tips-on-making-your-python-docker-images-more-robust-lighter-weight-and-more-secure-61876bcdc257
