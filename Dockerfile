# Base image
FROM python:3.8-slim

# installes required packages for our script
COPY requirements.txt /
RUN pip install -r /requirements.txt
# Copies your code file  repository to the filesystem
COPY entrypoint.py /entrypoint.py

# file to execute when the docker container starts up
ENTRYPOINT ["python", "entrypoint.py"]