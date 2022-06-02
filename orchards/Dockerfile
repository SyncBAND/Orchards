# pull official base image
FROM python:3.8-slim-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/scripts:${PATH}"

RUN pip install --upgrade pip
# packages required for setting up WSGI and scipy
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc make libc-dev python3-dev musl-dev

COPY requirements.txt $HOME/requirements.txt
RUN pip install --use-deprecated=legacy-resolver --no-cache-dir -r requirements.txt && \
    apt-get remove -y --purge make gcc build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

RUN adduser --system --group aero

# set work directory
RUN mkdir -p /home/aero/app
ENV HOME=/home/aero/app
WORKDIR $HOME

# copy project
COPY . $HOME

# give aero ownership to static folder
RUN mkdir -p $HOME/orchards/static && chown -R aero:aero $HOME/orchards/static

# create log file
RUN mkdir -p /var/log/uwsgi/ && touch /var/log/uwsgi/aero.log && chown aero:aero -R /var/log/uwsgi/

# Copy entrypoint
COPY entrypoint.sh $HOME/entrypoint.sh
RUN chmod +x $HOME/entrypoint.sh