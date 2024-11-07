# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Install Git
RUN apt-get update && apt-get install -y git

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir report

CMD python verifybibtex.py report/$BIBTEX_FILE
