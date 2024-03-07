# Base image - for python environments mostly Python
FROM python:3.11-slim

# set the working directory
WORKDIR /app

# install dependencies and src
COPY ./requirements.txt ./
COPY ./setup.py ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy the src to the folder
COPY ./src ./src

# Common pitfalls:
# 1) Filename has to be Dockerfile exactly. Otherwise it won't work.
