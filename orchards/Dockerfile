# pull official base image
FROM alpine:latest

ENV PACKAGES="\
    dumb-init \
    musl \
    libc6-compat \
    linux-headers \
    build-base \
    bash \
    git \
    ca-certificates \
    freetype \
    libgfortran \
    libgcc \
    libstdc++ \
    openblas \
    tcl \
    tk \
    libssl1.0 \
"

# install environment dependencies
RUN pip install --upgrade pip

ENV PYTHON_PACKAGES="\
    numpy \
    matplotlib \
    scipy \
    scikit-learn \
    pandas \
    nltk \
    Django \
    django-constance[database]==2.9.0 \
    plotly \
    python-decouple \
    Shapely \
    sklearn \
    requests \
    uWSGI \
" 

RUN addgroup -S aero && adduser -S aero -G aero

RUN apk add --no-cache --virtual build-dependencies python --update py-pip \
    && apk add --virtual build-runtime \
    build-base python-dev openblas-dev freetype-dev pkgconfig gfortran \
    && ln -s /usr/include/locale.h /usr/include/xlocale.h \
    && pip install --upgrade pip \
    && pip install --no-cache-dir $PYTHON_PACKAGES \
    && apk del build-runtime \
    && apk add --no-cache --virtual build-dependencies $PACKAGES \
    && rm -rf /var/cache/apk/*

# set work directory
RUN mkdir -p /home/aero/app
ENV HOME=/home/aero/app
WORKDIR $HOME

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