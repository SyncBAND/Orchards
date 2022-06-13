FROM frolvlad/alpine-python-machinelearning

# install psycopg2 and uwsgi dependencies
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev openssl-dev \
    && apk add libffi-dev python3-dev geos-dev \
    && rm -rf /var/lib/apt/lists/* 

RUN addgroup -S aero && adduser -S aero -G aero

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV $HOME/.local
ENV VENV_PIP $VIRTUAL_ENV/bin/pip
ENV PATH $VIRTUAL_ENV/bin:$PATH

# set work directory
RUN mkdir -p /home/aero/app
ENV HOME=/home/aero/app
WORKDIR $HOME

# copy project
COPY . $HOME

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r $HOME/requirements.txt

# give aero ownership to static folder
RUN mkdir -p $HOME/orchards/static && chown -R aero:aero $HOME/orchards/static

# create log file
RUN mkdir -p /var/log/uwsgi/ && touch /var/log/uwsgi/aero.log && chown aero:aero -R /var/log/uwsgi/

# wait until postres is ready
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait
RUN chmod +x /wait

# Copy entrypoint
COPY entrypoint.sh $HOME/entrypoint.sh
RUN chmod +x $HOME/entrypoint.sh