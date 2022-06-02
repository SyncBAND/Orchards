# pull official base image
FROM python:3.9.6-alpine

RUN addgroup -S aero && adduser -S aero -G aero

# install python and uwsgi dependencies
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers python3-dev musl-dev openssl-dev \
    && apk add libffi-dev \
    && rm -rf /var/lib/apt/lists/* 

# set work directory
RUN mkdir -p /home/aero/app
ENV HOME=/home/aero/app
WORKDIR $HOME

# install environment dependencies
RUN pip install --upgrade pip
RUN pip install cython
COPY requirements.txt $HOME/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV $HOME/.local
ENV VENV_PIP $VIRTUAL_ENV/bin/pip
ENV PATH $VIRTUAL_ENV/bin:$PATH

# copy project
COPY . $HOME

# give aero ownership to static folder
RUN mkdir -p $HOME/orchards/static && chown -R aero:aero $HOME/orchards/static

# create log file
RUN mkdir -p /var/log/uwsgi/ && touch /var/log/uwsgi/aero.log && chown aero:aero -R /var/log/uwsgi/

# Copy entrypoint
COPY entrypoint.sh $HOME/entrypoint.sh
RUN chmod +x $HOME/entrypoint.sh