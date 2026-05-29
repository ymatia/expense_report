# -----------------------------
# Stage 1a: Build frontend assets
# -----------------------------
FROM node:24 AS frontend-builder

WORKDIR /

# Copy only package files first (better caching)
COPY package.json ./
RUN npm install

# Copy the rest of your source
COPY src ./src
COPY vite.config.js ./

# Build the frontend
RUN npm run build

#############################
# Stage 1: Builder (Python deps + frpc for HaRP)
#############################
FROM python:3.12-slim-bookworm AS builder

WORKDIR /

RUN apt-get update && apt-get install -y curl ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /
RUN --mount=type=cache,target=/root/.cache/pip \
    python3 -m pip install --root-user-action=ignore -r /requirements.txt && rm /requirements.txt

# FRP client (required when HP_SHARED_KEY is set: bridges UDS to HaRP)
ARG FRP_VERSION=0.61.1
ARG FRP_AMD64_SHA256=bff260b68ca7b1461182a46c4f34e9709ba32764eed30a15dd94ac97f50a2c40
ARG FRP_ARM64_SHA256=af6366f2b43920ebfe6235dba6060770399ed1fb18601e5818552bd46a7621f8

RUN set -ex; \
    ARCH=$(uname -m); \
    if [ "$ARCH" = "aarch64" ]; then \
        FRP_ARCH="arm64"; \
        FRP_SHA256="${FRP_ARM64_SHA256}"; \
    else \
        FRP_ARCH="amd64"; \
        FRP_SHA256="${FRP_AMD64_SHA256}"; \
    fi; \
    FRP_URL="https://github.com/fatedier/frp/releases/download/v${FRP_VERSION}/frp_${FRP_VERSION}_linux_${FRP_ARCH}.tar.gz"; \
    curl -fsSL "${FRP_URL}" -o /tmp/frp.tar.gz; \
    ACTUAL_SHA256=$(sha256sum /tmp/frp.tar.gz | cut -d' ' -f1); \
    if [ "$ACTUAL_SHA256" != "$FRP_SHA256" ]; then \
        echo "Checksum verification failed for FRP v${FRP_VERSION} (${FRP_ARCH})"; \
        exit 1; \
    fi; \
    tar -C /tmp -xzf /tmp/frp.tar.gz; \
    cp /tmp/frp_${FRP_VERSION}_linux_${FRP_ARCH}/frpc /usr/local/bin/frpc; \
    chmod +x /usr/local/bin/frpc; \
    rm -rf /tmp/frp_${FRP_VERSION}_linux_${FRP_ARCH} /tmp/frp.tar.gz

#############################
# Stage 2: Runtime
#############################
FROM python:3.12-slim-bookworm

WORKDIR /

COPY --from=builder /usr/local/ /usr/local/

RUN apt-get update && apt-get install -y bash curl procps ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY ex_app /ex_app
# COPY --from=frontend-builder js/expense-report-main.mjs /ex_app/js/expense-report-main.js
COPY --from=frontend-builder js/* /ex_app/js/
# COPY --from=frontend-builder css/* /ex_app/css/
COPY --chmod=775 healthcheck.sh /
COPY --chmod=775 start.sh /

WORKDIR /ex_app/lib
ENTRYPOINT ["/start.sh", "python3", "main.py"]
HEALTHCHECK --interval=2s --timeout=2s --retries=300 CMD /healthcheck.sh
