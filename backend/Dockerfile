# pull official base image
FROM python:3.10

# set working directory
WORKDIR /web_app/backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV DEBUG=1

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean

# Copy dependencies from poetry
COPY pyproject.toml poetry.lock ./

# install python dependencie
RUN pip install --upgrade pip setuptools poetry
RUN poetry config virtualenvs.create false
RUN poetry export --dev --without-hashes --no-interaction --no-ansi -f requirements.txt -o requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# add app
COPY . /web_app/backend

RUN chmod +x /web_app/backend/entrypoint.sh