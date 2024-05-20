# Use the official Python 3.8 slim image as the base image
FROM python:3.8-slim

# Set the working directory within the container
WORKDIR /apirest_tutorial
# Copy the necessary files and directories into the container
COPY resources/ static/ util/ .env application.py requirements.txt /api-flask/
COPY resources/ /api-flask/resources/
COPY static/ /api-flask/static/
COPY util/ /api-flask/util/
COPY .env application.py requirements.txt  /api-flask/
