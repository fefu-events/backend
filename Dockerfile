# Pull base image
FROM python:3.10.2

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code/

# Install dependencies
COPY . /code/

RUN pip install poetry
RUN poetry install

EXPOSE 8000
