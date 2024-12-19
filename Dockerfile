
FROM python:3.11-slim-bookworm  as builder
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    gcc \
    git

ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 -

COPY ./poetry.lock ./pyproject.toml ./
COPY ./logger/ /shared/logger/

#the next 2 command are needed as long as we are in the development process of the package
RUN sed -i 's#logger = {path = "../../shared/logger", develop = true}#logger = {path = "../../shared/logger", develop = false}#' pyproject.toml
RUN poetry config virtualenvs.create false
RUN poetry lock

# Copy the shared package written in pyproject.toml

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --only main --no-dev

FROM python:3.11-slim-bookworm 
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libffi8 \
        libssl3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/local/lib/:$PATH"

# Copy the installed packages from the builder image
COPY --chown=1001:1001 --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
# Copy Flask and Gunicorn executables (CLI)
# COPY --chown=1001:1001 --from=builder /usr/local/bin/flask /usr/local/bin/flask
# COPY --chown=1001:1001 --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn
COPY --chown=1001:1001 --from=builder /usr/local/bin/ /usr/local/bin/

WORKDIR /opt/CTFd
COPY --chown=1001:1001 . /opt/CTFd

RUN useradd \
    --no-log-init \
    --shell /bin/bash \
    -u 1001 \
    ctfd \
    && mkdir -p /var/log/CTFd /var/uploads \
    && chown -R 1001:1001 /var/log/CTFd /var/uploads /opt/CTFd \
    && chmod +x /opt/CTFd/docker-entrypoint.sh

USER 1001
EXPOSE 8000
ENTRYPOINT ["/opt/CTFd/docker-entrypoint.sh"]
