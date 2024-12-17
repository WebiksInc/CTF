# Build FrontEnd files
FROM node:slim AS ui_files_builder
WORKDIR /opt/CTFd
#TBD: Copy only the theme files
COPY . /opt/CTFd

WORKDIR /opt/CTFd/CTFd/themes/ctfd-js
RUN npm install

# Build User Panel UI files
WORKDIR /opt/CTFd/CTFd/themes/core-beta
RUN npm install \
    && npm run build
# Build Admin Panel UI files
WORKDIR /opt/CTFd/CTFd/themes/admin
RUN npm install \
        && npm run build

FROM python:3.11-slim-bookworm AS build
WORKDIR /opt/CTFd

# hadolint ignore=DL3008
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libffi-dev \
        libssl-dev \
        git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY . /opt/CTFd

RUN pip install --no-cache-dir -r requirements.txt \
    && for d in CTFd/plugins/*; do \
        if [ -f "$d/requirements.txt" ]; then \
            pip install --no-cache-dir -r "$d/requirements.txt";\
        fi; \
    done;


FROM python:3.11-slim-bookworm AS release
WORKDIR /opt/CTFd

# hadolint ignore=DL3008
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libffi8 \
        libssl3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --chown=1001:1001 . /opt/CTFd 
RUN rm -rf /opt/CTFd/CTFd/themes/ 
COPY --from=ui_files_builder /opt/CTFd/CTFd/themes/admin/static /opt/CTFd/CTFd/themes/admin/static
COPY --from=ui_files_builder /opt/CTFd/CTFd/themes/admin/templates /opt/CTFd/CTFd/themes/admin/templates
COPY --from=ui_files_builder /opt/CTFd/CTFd/themes/core-beta/static /opt/CTFd/CTFd/themes/core-beta/static
COPY --from=ui_files_builder /opt/CTFd/CTFd/themes/core-beta/templates /opt/CTFd/CTFd/themes/core-beta/templates

RUN useradd \
    --no-log-init \
    --shell /bin/bash \
    -u 1001 \
    ctfd \
    && mkdir -p /var/log/CTFd /var/uploads \
    && chown -R 1001:1001 /var/log/CTFd /var/uploads /opt/CTFd \
    && chmod +x /opt/CTFd/docker-entrypoint.sh

COPY --chown=1001:1001 --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

USER 1001
EXPOSE 8000
ENTRYPOINT ["/opt/CTFd/docker-entrypoint.sh"]
