FROM python:3.12-slim-bookworm AS builder

COPY requirements.txt /
RUN --mount=type=cache,target=/root/.cache/pip \
    python3 -m pip install --root-user-action=ignore -r /requirements.txt && rm /requirements.txt

FROM python:3.12-slim-bookworm

COPY --from=builder /usr/local/ /usr/local/
RUN apt-get update && apt-get install -y curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ADD /ex_app/li[b] /ex_app/lib
COPY --chmod=775 healthcheck.sh /
COPY --chmod=775 start.sh /

WORKDIR /ex_app/lib
ENTRYPOINT ["/start.sh", "python3", "main.py"]
# start-period: allow pip/import + uvicorn bind before failures count
HEALTHCHECK --interval=5s --timeout=5s --start-period=40s --retries=12 CMD /healthcheck.sh
