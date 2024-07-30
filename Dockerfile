FROM python:3.12.3-slim-bullseye as app

### WORKDIR IN SAAS UPDATE IS /app - change volumes and nginx files if you change from /scrapegod to /app
WORKDIR /app

# ENV INSTALL_PATH /scrapegod
# RUN mkdir -p $INSTALL_PATH

# WORKDIR $INSTALL_PATH

# COPY requirements.txt requirements.txt
# # RUN pip install -r requirements.txt

# # TO MIRROS CHANGES FROM
# COPY . /app

ENV BUILD_DEPS="build-essential" \
	APP_DEPS="curl libpq-dev"

# RUN apt-get update && apt-get install -qq -y \
#   build-essential libpq-dev --no-install-recommends 

# Install ghostscript
# RUN apt-get install --no-install-recommends -y \
#   ghostscript -y \
#   && ln -s pdf_creator.py pdfc
#   && echo export=/absolute/path/of/the/folder/script/:$PATH >> ~/.bash_profile

RUN apt-get update \
	&& apt-get install -y ${BUILD_DEPS} ${APP_DEPS} --no-install-recommends \
	wkhtmltopdf wget ghostscript unzip curl chromium fonts-liberation gnupg2 poppler-utils -y git \
	# chromium fonts-liberation gnupg2 needed for chrome
	&& ln -s pdf_creator.py pdfc \
	#   && pip install -r requirements.txt \
	&& rm -rf /var/lib/apt/lists/* \
	&& rm -rf /usr/share/doc && rm -rf /usr/share/man \
	#   && apt-get purge -y --auto-remove ${BUILD_DEPS} \
	&& apt-get clean

RUN python3 -m pip install --upgrade pip


# Add JAVA for tabula-py
###
RUN set -eux; \
	apt-get update; \
	apt-get install -y --no-install-recommends \
	# utilities for keeping Debian and OpenJDK CA certificates in sync
	ca-certificates p11-kit \
	; \
	rm -rf /var/lib/apt/lists/*

# Default to UTF-8 file.encoding
ENV LANG C.UTF-8

RUN useradd --create-home python \
	&& mkdir -p /home/python/.cache/pip && chown python:python -R /home/python /app

USER python

COPY --chown=python:python requirements*.txt ./
COPY --chown=python:python bin/ ./bin
# COPY --chown=python:python bin/pip3-install ./bin/pip3-install
# COPY --chown=python:python bin/docker-entrypoint-web ./bin/docker-entrypoint-web

# If returning not found error here on Windows, ensure Line Endings are LF not CRLF for Dockerfile and files in bin/
RUN chmod 0755 bin/* && bin/pip3-install

### Set to production in production
ARG FLASK_ENV="production"
ENV FLASK_ENV="${FLASK_ENV}" \
	FLASK_APP="scrapegod.app" \
	FLASK_SKIP_DOTENV="true" \
	PYTHONUNBUFFERED="true" \
	PYTHONPATH="." \
	PATH="${PATH}:/home/python/.local/bin" \
	USER="python"


COPY --chown=python:python . .

EXPOSE 8000

