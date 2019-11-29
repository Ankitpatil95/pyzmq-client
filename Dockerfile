FROM python:3-slim

# make directory to copy code
RUN mkdir /code

# set work directory
WORKDIR /code

# copy project
COPY . .

# install dependencies
RUN pip install -r /code/requirements.txt --no-cache-dir

