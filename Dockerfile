# Base image - for python environments mostly Python
FROM python:3.11-slim

# set the working directory
WORKDIR /code

# install dependencies
COPY ./requirements.txt ./


RUN pip install --no-cache-dir --upgrade -r requirements.txt
# RUN pip install --no-cache-dir --upgrade -r requirements.txt
# --no-cache-dir - because docker has its own cache
# Docker can cache each step, so it's a good practice to have requirements separately (because they don't change so often)



# copy the src to the folder
COPY ./src ./src

# start the server
# as a list of strings 
# src.main:app -> because we are in the main dyrectory
# CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
# For docker you usually specify host 0.0.0.0 and then you can acces this from your local host on port 80


# Common pitfalls:
# 1) Filename has to be Dockerfile exactly. Otherwise it won't work.
