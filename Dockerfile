FROM python:3.9.1-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy project files
WORKDIR /app
COPY . .

# install utilities
RUN apt-get update && apt-get install -y netcat

# install python dependencies from Pipfile
RUN pip install --upgrade pip
RUN python -m pip install pipenv
RUN pipenv install --deploy --system

RUN chmod +x /app/run_wsgi.sh