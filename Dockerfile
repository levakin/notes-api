FROM python:3.6-slim
LABEL maintainer "<levakin levakin@protonmail.com>"
WORKDIR /app
ADD . /app
RUN pip install pipenv && pipenv install --system --deploy --ignore-pipfile
EXPOSE 8080