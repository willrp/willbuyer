FROM python:3.7-slim

ENV PIPENV_DONT_LOAD_ENV=1
ENV PIPENV_VERBOSITY=-1
ENV PIPENV_IGNORE_VIRTUALENVS=1

RUN mkdir -p /usr/src
WORKDIR /usr/src

COPY . /usr/src

RUN apt-get update && apt-get install -y \
    build-essential \
    python-dev \
    libpq-dev \
    curl

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv lock -r > requirements.txt
RUN pip install -r requirements.txt --no-cache-dir
RUN pip install gunicorn
RUN rm backend-test.py backend-dev.py requirements.txt Pipfile Pipfile.lock


RUN curl -sL https://deb.nodesource.com/setup_13.x | bash
RUN apt-get install -y nodejs

WORKDIR /usr/src/frontend
RUN npm install && npm run build
RUN rm -r css html img js node_modules
RUN rm *.json *.js .flowconfig

WORKDIR /usr/src
CMD ["gunicorn", "-w", "4", "backend:create_app('production')"]