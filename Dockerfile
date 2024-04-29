# Base image - typically Python for Python dev environments
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install dependencies and source
COPY ./requirements.txt ./
COPY ./setup.py ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy src package codes to the container
COPY ./src ./src

# Common pitfalls:
# 1) Filename has to be Dockerfile exactly. Otherwise it won't work.
# 2) You must copy ./setup.py to install the src package