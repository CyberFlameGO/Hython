
# ---- Base python ----
FROM python:3.6 AS base
FROM alpine:3.7

# VERSIONS
ENV ALPINE_VERSION=3.7 \
    PYTHON_VERSION=3.6.5

# PATHS
ENV PYTHON_PATH=/usr/lib/python$PYTHON_VERSION \
    PATH="/usr/lib/python$PYTHON_VERSION/bin/:${PATH}"
# Create app directory
WORKDIR /app

# ---- Dependencies ----
FROM base AS dependencies  
# install app dependencies
RUN pip install -r requirements.txt

# ---- Copy Files/Build ----
FROM dependencies AS build  
WORKDIR /app
COPY . /app
# Build / Compile if required

# --- Release with Alpine ----
FROM python:3.6-alpine3.7 AS release  
# Create app directory
WORKDIR /app

COPY --from=dependencies /app/requirements.txt ./
COPY --from=dependencies /root/.cache /root/.cache

# Install app dependencies
# RUN pip install -r requirements.txt IDK WHY THIS IS FUCKED?!?!?!
COPY --from=build /app/ ./

RUN set -ex ;\
    # find MAJOR and MINOR python versions based on $PYTHON_VERSION
    export PYTHON_MAJOR_VERSION=$(echo "${PYTHON_VERSION}" | rev | cut -d"." -f3-  | rev) ;\
    export PYTHON_MINOR_VERSION=$(echo "${PYTHON_VERSION}" | rev | cut -d"." -f2-  | rev) ;\
    # replacing default repositories with edge ones
    echo "http://dl-cdn.alpinelinux.org/alpine/v$ALPINE_VERSION/community" >> /etc/apk/repositories ;\
    echo "http://dl-cdn.alpinelinux.org/alpine/v$ALPINE_VERSION/main" >> /etc/apk/repositories ;\

    # Add the packages, with a CDN-breakage fallback if needed
    apk add --no-cache $PACKAGES || \
        (sed -i -e 's/dl-cdn/dl-4/g' /etc/apk/repositories && apk add --no-cache $PACKAGES) ;\
    # Add packages just for the python build process with a CDN-breakage fallback if needed
    apk add --no-cache --virtual .build-deps $PYTHON_BUILD_PACKAGES || \
        (sed -i -e 's/dl-cdn/dl-4/g' /etc/apk/repositories && apk add --no-cache --virtual .build-deps $PYTHON_BUILD_PACKAGES) ;\

    # turn back the clock -- so hacky!
    echo "http://dl-cdn.alpinelinux.org/alpine/v$ALPINE_VERSION/main/" > /etc/apk/repositories ;\
    # echo "@community http://dl-cdn.alpinelinux.org/alpine/v$ALPINE_VERSION/community" >> /etc/apk/repositories ;\
    # echo "@testing http://dl-cdn.alpinelinux.org/alpine/v$ALPINE_VERSION/testing" >> /etc/apk/repositories ;\
    # echo "@edge-main http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories ;\

    # use pyenv to download and compile specific python version
    git clone --depth 1 https://github.com/pyenv/pyenv /usr/lib/pyenv ;\
    PYENV_ROOT=/usr/lib/pyenv /usr/lib/pyenv/bin/pyenv install $PYTHON_VERSION ;\
    # move specific version to correct path delete pyenv, no longer needed
    mv /usr/lib/pyenv/versions/$PYTHON_VERSION/ $PYTHON_PATH ;\
    rm -rfv /usr/lib/pyenv ;\
    # change the path on the header of every file from PYENV_ROOT to PYTHON_PATH
    cd $PYTHON_PATH/bin/ && sed -i "s+/usr/lib/pyenv/versions/$PYTHON_VERSION/+$PYTHON_PATH/+g" * ;\
    # delete binary "duplicates" and replace them with symlinks
    # this also optimizes space since they are actually the same binary
    rm -f $PYTHON_PATH/bin/python$PYTHON_MAJOR_VERSION \
          $PYTHON_PATH/bin/python$PYTHON_MINOR_VERSION \
          $PYTHON_PATH/bin/python$PYTHON_MAJOR_VERSION-config \
          $PYTHON_PATH/bin/python$PYTHON_MINOR_VERSION-config ;\
    ln -sf $PYTHON_PATH/bin/python $PYTHON_PATH/bin/python$PYTHON_MAJOR_VERSION ;\
    ln -sf $PYTHON_PATH/bin/python $PYTHON_PATH/bin/python$PYTHON_MINOR_VERSION ;\
    ln -sf $PYTHON_PATH/bin/python-config $PYTHON_PATH/bin/python$PYTHON_MAJOR_VERSION-config ;\
    ln -sf $PYTHON_PATH/bin/python-config $PYTHON_PATH/bin/python$PYTHON_MINOR_VERSION-config ;\
    # delete files to to reduce container size
    # tips taken from main python docker repo
    find /usr/lib/python$PYTHON_VERSION -depth \( -name '*.pyo' -o -name '*.pyc' -o -name 'test' -o -name 'tests' \) -exec rm -rf '{}' + ;\

    # remove build dependencies and any leftover apk cache
    apk del --no-cache --purge .build-deps ;\
    rm -rf /var/cache/apk/*

# since we will be "always" mounting the volume, we can set this up
ENTRYPOINT ["/usr/bin/dumb-init"]
CMD ["python"]
